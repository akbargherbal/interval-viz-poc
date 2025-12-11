Over the weekend, I went through the Tenant Guide we drafted last session. It’s of the highest quality, with almost nothing to add except a couple of minor points:

1. I’m considering creating static mockup templates for various UI elements— like modals and the like, the main algorithm page, etc.—to illustrate our point of view by example, not just through writing (Tenant Guide). This will help prevent decision fatigue later as we scale things up and allow frontend developers (LLMs) to focus on the critical parts rather than the cosmetics. For example, we should establish that the buttons in the prediction modal must have different colors (they are currently all the same). Frontend developers can choose whatever theme color suits them, but we should define general guidelines consistent with the Tenant Guide.

2. Lead by example—eat our own dog food. We should test the principles outlined in the Tenant Guide on the algorithms we’ve built so far and ensure we are following the rules we established. We should dedicate at most two sessions to the two algorithms we’ve built.

3. Once we get points 1–3 right in our current implementation, we should make this an official standard for all future algorithms to follow.

4. Update `Phased_Plan_v1.4.0.md` with an addendum.

5. Update `README.md`, since it is now obsolete and was last updated during the PoC stage.

All the above will likely take three to four sessions.
