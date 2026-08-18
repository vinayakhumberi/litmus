# Design a Collaborative Document Editor

**How to use this document:** this is a worked answer to a real interview prompt, structured as the steps you'd actually narrate in a 45-minute round — applying the general frontend system design framework to this specific question. Every major decision includes an explicit **why**, and the alternative that was considered and rejected, because that reasoning — not the final diagram — is what's actually being evaluated. A condensed rehearsal summary is at the end.

---

## Step 0 — Scope the Prompt (~2-3 min)

**What to say:** "Before I start designing, I want to bound the scope. Is this closer to a Google-Docs-style rich text editor, or something more constrained like a shared plain-text notes app? What's the target scale — tens of concurrent editors per document, or hundreds? Is offline editing in scope, or can I assume a mostly-connected client?"

**Why ask this first:** "collaborative document editor" spans wildly different systems depending on the answers — a plain-text pair-programming tool and a full rich-text Google Docs clone have almost nothing in common architecturally below the surface. Designing before scoping risks solving the wrong problem entirely, which is a worse outcome than solving a smaller problem well.

**Scope assumed for the rest of this walkthrough** (state this out loud, don't just silently assume it):
- Rich text editing (bold/italic/lists/headings) — not just plain text.
- Up to ~20 concurrent editors per document — small-group real-time collaboration, not thousands of simultaneous viewers.
- Real-time sync is the P0 requirement; offline editing is explicitly named as an extension, discussed in cross-cutting concerns but not the primary design target.
- Web only — no native mobile client to design for.

---

## Step 1 — Requirements (~3-5 min)

| Type | Requirement |
|---|---|
| **Functional** | Multiple users edit the same document simultaneously and see each other's changes in near real time |
| **Functional** | Users see each other's cursor position and text selection ("presence") |
| **Functional** | Standard rich text formatting, undo/redo per user |
| **Functional** | Document persists and can be reopened later with full history intact |
| **Non-functional** | Perceived edit latency for the local user must be near-zero — typing must never wait on the network |
| **Non-functional** | Remote edits should generally appear within a few hundred milliseconds under normal network conditions |
| **Non-functional** | All clients must converge to the identical final document, regardless of the order operations arrive in |
| **Non-functional** | Graceful degradation on a dropped connection — no data loss, no silent divergence |

> **Why these non-functional requirements specifically:** the "near-zero local latency" and "guaranteed convergence" requirements are what actually drive the entire sync-protocol decision in Step 3 — naming them explicitly here means the interviewer sees the deep dive is justified by a stated requirement, not just a favorite technology.

---

## Step 2 — High-Level Architecture (~10-15 min)

At the highest level: each client keeps its own local, editable copy of the document, edits apply to that local copy immediately, and a background sync mechanism reconciles changes across clients through a lightweight relay server. The server's job is to relay and persist, not to be the single source of truth clients must round-trip to before showing a change — that distinction is the reason typing never has to wait on the network.

```mermaid
graph TD
    A["User types a character"] --> B["Apply edit optimistically<br>to local document model"]
    B --> C["Re-render editor immediately<br>no network wait"]
    B --> D["Generate a sync operation<br>describing the edit"]
    D --> E["Send operation to<br>collaboration server over WebSocket"]
    E --> F{"Server validates<br>auth and document permissions"}
    F -- "Authorized" --> G["Server relays the operation<br>to every other connected client"]
    F -- "Unauthorized" --> H["Reject - client shows<br>a sync error state"]
    G --> I["Each remote client merges<br>the operation into its local model"]
    I --> J["Remote editors re-render<br>with the new content"]
    E --> K["Server periodically persists<br>a document snapshot"]

    classDef local fill:#2f855a,stroke:#9ae6b4,color:#fff
    classDef server fill:#2b6cb0,stroke:#90cdf4,color:#fff
    classDef decision fill:#805ad5,stroke:#d6bcfa,color:#fff

    class A,B,C,D local
    class E,G,K server
    class F decision
    class H,I,J local
```

**Why the server is a relay, not an authority the client waits on:** if every keystroke had to round-trip to the server and back before the local editor updated, typing would feel exactly as laggy as the network — unacceptable per the latency requirement above. Treating the local model as immediately-correct (optimistic) and reconciling in the background is what makes this feel instant regardless of network conditions.

> **Key takeaway:** the architecture's core shape — local-first apply, background sync, server as relay/persistence rather than gatekeeper — falls directly out of the "near-zero local latency" requirement from Step 1. This is worth stating explicitly in the interview: the architecture isn't a default, it's a consequence of a specific requirement.

---

## Step 3 — Data Model & Sync Protocol Deep Dive (~15-20 min)

This is the hard part of the problem, and where the interview signal actually concentrates. If every client applies edits locally and independently, and those edits can arrive at other clients in any order, the core question is: **how do all clients guarantee they converge on the exact same final document, without a central server dictating a strict operation order?**

### The central decision: CRDTs vs. Operational Transformation

| | **CRDTs** (Conflict-free Replicated Data Types) | **Operational Transformation (OT)** |
|---|---|---|
| **Convergence guarantee** | Mathematically guaranteed by the data structure itself — operations commute or are designed to merge deterministically | Guaranteed by a transform algorithm that rewrites operations against each other in the correct order |
| **Server requirement** | Server can be a "dumb" relay — no need to see or understand operation order | Requires a central server to sequence and transform operations correctly — genuinely peer-to-peer OT is very hard to get right |
| **Offline / reconnect behavior** | Naturally merge-friendly — a client can accumulate local operations indefinitely and merge them whenever it reconnects | Harder — the transform algorithm assumes a mostly-live operation stream; long offline periods complicate the transform math significantly |
| **Complexity** | Complexity lives in the data structure and its merge function, implemented once and reused | Complexity lives in the transform functions, which must correctly handle every pair of operation types — historically a major source of subtle bugs |
| **Real-world adopters** | Figma, Notion, Yjs-based editors | Google Docs (historically), Google Wave |

**Decision: CRDT**, given the requirements scoped in Step 1. A dumb-relay server is simpler to reason about and cheaper to run at this scale, and the "graceful degradation on dropped connections, no data loss" requirement maps directly onto CRDTs' natural tolerance for a client rejoining after an arbitrary gap and merging cleanly — which is a materially harder problem to solve well with OT.

> **When I'd choose OT instead:** if the requirements named a strict, centrally-defined operation order as a hard requirement (for example, an audit log that must reflect a single canonical sequence of edits across all users, not just an eventually-consistent merged result), OT's server-mediated sequencing would be the better fit. Naming this condition explicitly is what separates "I know CRDTs exist" from "I understand the actual trade-off."

### The concrete data structure: a sequence CRDT for text

For rich text specifically, each character (or run of characters) gets a unique, stable position identifier that doesn't change when other characters are inserted or deleted around it — commonly implemented as a fractional-index or a tree-based positioning scheme (this is the approach libraries like Yjs use under the hood). Two clients inserting at "the same visual position" concurrently naturally end up with different, well-ordered position identifiers, so there's no ambiguity to resolve — the CRDT's merge rule (a deterministic tie-breaker, e.g., by client ID, for genuinely simultaneous inserts at the same position) produces the same final ordering on every client without any negotiation.

```typescript
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';

const doc = new Y.Doc();
const ytext = doc.getText('content'); // the shared, CRDT-backed text type

// Every local edit to ytext is automatically diffed into CRDT operations and
// sent over this connection; remote operations are applied and merged the
// same way, using the position-identifier scheme described above internally.
const provider = new WebsocketProvider('wss://sync.example.com', 'doc-id', doc);

ytext.observe(() => {
  // Fires for both local and remote-merged changes - re-render from here
  renderEditorContent(ytext.toString());
});
```

### The full round-trip: local edit to remote convergence

```mermaid
sequenceDiagram
    participant A as "Client A"
    participant S as "Collaboration Server"
    participant B as "Client B"

    A->>A: "User A types 'hello' at a position"
    A->>A: "Apply optimistically to local CRDT model"
    A->>S: "Send insert operation"
    B->>B: "User B types 'world' at the same position, concurrently"
    B->>B: "Apply optimistically to local CRDT model"
    B->>S: "Send insert operation"
    S->>A: "Relay B's operation to A"
    S->>B: "Relay A's operation to B"
    A->>A: "CRDT merges B's op deterministically - no manual conflict resolution needed"
    B->>B: "CRDT merges A's op deterministically - same final order as A"
    Note over A,B: "Both clients converge to the identical final document"

    Note over S: "Client B's connection drops"
    B--xS: "WebSocket disconnects"
    B->>B: "Editing continues locally - operations queue up"
    B->>S: "Reconnects, resyncs state and replays queued operations"
    S->>B: "Sends any operations B missed while disconnected"
    B->>B: "Merges missed operations - converges again"
```

> **Key takeaway:** the reconnect flow in the second half of this diagram isn't a special case bolted on — it's the same merge function used for every normal concurrent edit, just applied to a larger batch of queued operations. That reuse is a direct payoff of the CRDT decision from earlier: there's no separate "reconciliation algorithm" to design for the offline case.

---

## Step 4 — Presence & Awareness (~5 min)

Cursor positions, text selections, and "who's currently viewing this document" are architecturally distinct from the document content itself, and deliberately handled differently.

**Why presence is not part of the CRDT document state:** presence is ephemeral and last-write-wins by nature — if User A's cursor position update from two seconds ago arrives after a more recent one, the old one should simply be discarded, not merged. Running this through the same conflict-free merge machinery as document content would be unnecessary complexity for data that doesn't need durability or conflict resolution at all. Yjs ships exactly this as a separate primitive — the awareness protocol — piggybacked on the same connection but with no merge function at all.

> **Key takeaway:** not everything flowing through the same connection needs the same consistency guarantees — recognizing which data needs CRDT-grade convergence and which just needs "latest wins, ephemeral" is itself a design decision worth stating explicitly.

### Keeping a remote cursor valid as the document changes underneath it

Broadcasting "latest wins, ephemeral" only solves *who has the newest cursor update* — it doesn't solve a separate, easy-to-miss problem: **a cursor position stored as a raw character index goes stale the instant anyone edits the document before that point.** If User B's cursor is at index 42 and User A inserts 5 characters at index 10, index 42 is now pointing at the wrong character. A plain integer has no way to know the document shifted under it.

This is why cursor position needs the *same kind of data type* as document content — anchored to a stable position identifier, not a raw offset. Yjs's `RelativePosition` is exactly this: it anchors to a specific CRDT item rather than an index, so it can be resolved back to a correct index against whatever the document's current state is, no matter what edits happened in between.

```typescript
import { Awareness } from 'y-protocols/awareness';

const awareness = provider.awareness; // WebsocketProvider exposes this by default

// Sender: anchor the cursor to a CRDT item, not a raw index
function broadcastCursor(selectionOffset: number) {
  const relPos = Y.createRelativePositionFromTypeIndex(ytext, selectionOffset);
  awareness.setLocalStateField('cursor', Y.encodeRelativePosition(relPos));
}

// Receiver: resolve it back to a real index against MY current document state -
// correct even if edits landed between when it was sent and when it's read
awareness.on('change', () => {
  for (const state of awareness.getStates().values()) {
    const relPos = Y.decodeRelativePosition(state.cursor);
    const absPos = Y.createAbsolutePositionFromRelativePosition(relPos, doc);
    if (absPos) updateRemoteCursorIndex(state.userId, absPos.index);
  }
});
```

### Rendering cursors without re-rendering the document

Resolving the index correctly is only half the problem — the other half is not re-rendering the entire document every time a remote cursor moves. Cursor updates are high-frequency (every keystroke, every arrow key, potentially every mouse move), so wiring the resolved index directly into the same state that drives the document's text content would re-render the whole editor on every twitch of every collaborator's cursor — a real, self-inflicted performance bug, not a detail to wave away.

The fix is architectural, not a memoization afterthought: resolved cursor positions live in their own small, isolated piece of state, rendered as a thin absolutely-positioned overlay above the text (converting the resolved index to pixel coordinates via `range.getBoundingClientRect()`). Only that overlay re-renders on a cursor move; the document content re-renders only when content itself actually changes. This is the same state-isolation principle behind `React.memo`-driven optimization, applied here at the architecture level instead of a component-memoization level — a high-frequency, low-importance value should never sit in the same state as something expensive and mostly-unrelated.

> **Key takeaway:** cursor sync is really two separate problems wearing one trenchcoat — keeping the *position value* correct as the document mutates (a data-type problem, solved by relative positions), and keeping the *rendering* of that position cheap (a state-isolation problem, solved by a separate overlay). Conflating them into "just broadcast the cursor index" misses both.

---

## Step 5 — Cross-Cutting Concerns (~5 min)

| Concern | What to say |
|---|---|
| **Performance** | For very large documents, virtualize rendering of off-screen content, and debounce snapshot persistence rather than persisting on every keystroke |
| **Accessibility** | Remote edits appearing while a screen-reader user is mid-task need careful ARIA live-region tuning — announcing every remote keystroke would be unusable; batch and summarize instead ("2 changes from Alex") |
| **Security** | The WebSocket channel must be authenticated per-document, not just per-user, since document-level permissions can differ from account-level auth; user-generated rich text content must be sanitized against XSS before rendering |
| **Offline resilience** | This is where the CRDT decision pays off directly — queued local operations replay and merge cleanly on reconnect, covered in Step 3's diagram |
| **Testing** | Deterministic merge-convergence property tests (given any operation ordering, assert all replicas converge identically) are the testing layer unique to this kind of system — standard unit tests don't exercise concurrent-merge correctness |

---

## Step 6 — Trade-offs & Wrap-up (~3-5 min)

**Alternatives considered and explicitly rejected:**

- **A naive "last write wins, whole document" approach** — rejected immediately: two users editing different parts of the document simultaneously would silently destroy one user's changes entirely, which fails the "no data loss" requirement outright.
- **Broadcasting raw operations without a CRDT merge function** — rejected: without a principled merge rule, concurrent edits at the same position produce genuinely ambiguous results that differ depending on arrival order, breaking the convergence guarantee.
- **Operational Transformation** — not rejected outright, but deprioritized given this specific requirement set; explicitly named as the better choice under a different, stricter ordering requirement (see Step 3).

**What I'd revisit given more time or scale:**
- Very large documents (tens of thousands of words) likely need the CRDT structure itself sharded or paginated, since a single flat sequence CRDT's metadata overhead grows with document size.
- Persistence is described here as "the same collaboration server," but at real scale I'd split persistence into its own service so a spike in relay traffic doesn't compete with write throughput to storage.
- Rich embedded objects (comments anchored to text ranges, inline images) introduce their own merge semantics beyond plain text and would need a follow-up design pass.

---

## 60-Second Rehearsal Summary

- **Scope:** rich text, ~20 concurrent editors, real-time is P0, offline is an extension.
- **Architecture:** local-first optimistic apply → background sync via a relay server → server persists snapshots. Server is a relay, not a gatekeeper, because local latency must be near-zero.
- **Sync protocol:** CRDT over OT, because the requirements favor a dumb-relay server and graceful offline/reconnect behavior over strict central ordering. Sequence CRDT with stable per-character position IDs; deterministic merge means no negotiation needed.
- **Presence:** separate ephemeral, last-write-wins channel — deliberately not run through the CRDT merge path.
- **Cross-cutting:** batched a11y announcements for remote edits, per-document WebSocket auth, debounced persistence, convergence property tests as the testing layer unique to this system.
- **Rejected alternatives named explicitly:** naive last-write-wins (data loss), raw op broadcast with no merge function (ambiguous convergence), OT (right call only under a stricter ordering requirement than this one).
