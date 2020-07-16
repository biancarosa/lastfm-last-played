# Contributor Guidelines

  
## Pull Requests

- **DO** give PRs short-but-descriptive names (e.g. &quot;Improve code coverage for System.Console by 10%&quot;, not &quot;Fix #1234&quot;).
- **DO NOT** submit &quot;work in progress&quot; PRs. A PR should only be submitted when it is considered ready for review and subsequent merging by the contributor.
- **DO** tag any users that should know about and/or review the change.
- **DO** submit all code changes via pull requests (PRs) rather than through a direct commit. PRs will be reviewed and potentially merged by the repo maintainers after a peer review that includes at least one maintainer.
- **DO** ensure each commit successfully builds. The entire PR must pass all tests in the Continuous Integration (CI) system before it&#39;ll be merged.
- **DO NOT** mix independent, unrelated changes in one PR. Separate real product/test code changes from larger code formatting/dead code removal changes. Separate unrelated fixes into separate PRs, especially if they are in different assemblies.
- **DO** address PR feedback in an additional commit(s) rather than amending the existing commits, and only rebase/squash them when necessary. This makes it easier for reviewers to track changes. If necessary, squashing should be handled by the merger using the &quot;squash and merge&quot; feature, and should only be done by the contributor upon request.

## DOs and DO NOTs

- **DO** follow our git style guide
- **DO** give priority to the current style of the project or file you&#39;re changing even if it diverges from the general guidelines
- **DO** include tests when adding new features. When fixing bugs, start with adding a test that highlights how the current behavior is broken
- **DO** keep the discussions focused. When a new or related topic comes up it&#39;s often better to create a new issue than to side track the discussion
- **DO NOT** make PRs for style changes
- **DO NOT** surprise us with big pull requests. Instead, file an issue and start a discussion so we can agree on a direction before you invest a large amount of time working on it
- **DO NOT** add API additions without filing an issue and discussing with us first



## API Change Review Process

- **Contributor opens an issue.** The issue description should contain a speclet that represents a sketch of the new APIs, including samples on how the APIs are being used. The goal isn&#39;t to get a complete API list, but a good handle on how the new APIs would roughly look like and in what scenarios they are being used.
- **Community discusses the proposal.** If changes are necessary, the contributor is encouraged to edit the issue description. This allows folks joining later to understand the most recent proposal. To avoid confusion, the contributor should maintain a tiny change log, like a bolded &quot;Updates:&quot; followed by a bullet point list of the updates that were being made.
- **Issue is tagged as &quot;Accepting PRs&quot;.** Once the contributor and project owner agree on the overall shape and direction, the project owner tags the issue as &quot;Accepting PRs&quot;. The contributor should indicate whether they will be providing the PR or only contributed the idea.
- **Pull request is being created.** Once the contributor believes the implementation is ready for review, he/she creates a pull request, referencing the issue created in the first step.
- **Pull request is being reviewed.** The community reviews the code for the pull request. The review should focus on the code changes and architecture – not the APIs themselves. Once at least two project owners give their OK, the PR is considered good to go.
- **Owner makes decision.**  When the owner believes enough information is available to make a decision, she will update the issue accordingly:
- **Mark for review.**  If the owner believes the proposal is actionable, she will label the issue with api-ready-for-review.
- **Close as not actionable.**  In case the issue didn&#39;t get enough traction to be distilled into a concrete proposal, she will close the issue.
- **Close as won&#39;t fix as proposed.**  Sometimes, the issue that is raised is a good one but the owner thinks the concrete proposal is not the right way to tackle the problem. In most cases, the owner will try to steer the discussion in a direction that results in a design that we believe is appropriate. However, for some proposals the problem is at the heart of the design which can&#39;t easily be changed without starting a new proposal. In those cases, the owner will close the issue and explain the issue the design has.
- **Close as won&#39;t fix.**  Similarly, if proposal is taking the product in a direction we simply don&#39;t want to go, the issue might also get closed. In that case, the problem isn&#39;t the proposed design but in the issue itself.
- **API gets reviewed.**  In the review, we&#39;ll take notes and provide feedback. After the review, we&#39;ll publish the notes in the API review repository. Multiple outcomes are possible:
- **Approved.**  In this case the label api-ready-for-review is replaced with api-approved.
- **Needs work.**  In case we believe the proposal isn&#39;t ready yet, we&#39;ll replace the label api-ready-for-review with api-needs-work.
- **Rejected.**  In case we believe the proposal isn&#39;t a direction we want to go after, we simply write a comment and close the issue.
- **Pull request is merged.** When there are no issues – or the issues were addressed by the contributor, the PR is merged.
