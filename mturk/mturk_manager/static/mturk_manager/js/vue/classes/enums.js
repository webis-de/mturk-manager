export const STATUS_BLOCK = {
  NONE: 1,
  SOFT: 2,
  HARD: 3,
};
export const STATUS_EXTERNAL = {
  APPROVED: 0,
  REJECTED: 1,
  APPROVED_OVERRIDDEN: 2,
};
export const STATUS_INTERNAL = {
  APPROVED: 0,
  REJECTED: 1,
};

export const DESCRIPTIONS = {
  TITLE_HIT:
    'The title of the HIT. A title should be short and descriptive about the kind of task the HIT contains. On the Amazon Mechanical Turk web site, the HIT title appears in search results, and everywhere the HIT is mentioned.',
  DESCRIPTION_HIT:
    'A general description of the HIT. A description includes detailed information about the kind of task the HIT contains. On the Amazon Mechanical Turk web site, the HIT description appears in the expanded view of search results, and in the HIT and assignment screens. A good description gives the user enough information to evaluate the HIT before accepting it.',
  REWARD_HIT:
    'The US Dollar amount the Requester will pay a Worker for successfully completing the HIT.',
  ASSIGNEMENTS_MAX_HIT:
    'The number of times the HIT can be accepted and completed before the HIT becomes unavailable.',
  LIFETIME_HIT:
    'An amount of time, in seconds, after which the HIT is no longer available for users to accept. After the lifetime of the HIT elapses, the HIT no longer appears in HIT searches, even if not all of the assignments for the HIT have been accepted.',
  DURATION_HIT:
    'The amount of time, in seconds, that a Worker has to complete the HIT after accepting it. If a Worker does not complete the assignment within the specified duration, the assignment is considered abandoned. If the HIT is still active (that is, its lifetime has not elapsed), the assignment becomes available for other users to find and accept.',
  KEYWORDS_HIT:
    'One or more words or phrases that describe the HIT. These words are used in searches to find HITs.',
};
