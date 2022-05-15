## Features:
- Mostly used whenever we need inter application connectivity. Can transfer events from various SaaS applications to various targets.
    It can be also used to capture events from various 3rd party SaaS applications. 

- It was released in late 2019. Based on cloudwatch events.

- Eventbridge has a schema registry which allows automatic discovery and publishing of schema of the events being sent. So in case there's
    some change, that needn't be manually conveyed.

- Eventbridge gets an event which is an indicator for any change, and applies a rule to route the event to a target.
    Rules match events to targets based on the event structure(called as event pattern) or based on schedule.

- All events that come to eventbridge are associated with an event bus. Rules are tied to a single event bus, so they can only be applied 
    to events on that event bus.

- Eventbridge also has options to set HTTP endpoints as targets for rules using API destinations.

- There is also option of modifying/customizing the event in the event-bridge before sending it to the target.

- We can also save/archive the events and replay them later. Mostly useful for testing scenarios.

- Event bridge can be used when we need some task to run every on a scheduled basis. However scheduled expression support is only available
    on the default event bus, and not on any custom event bus. It is possible to add event pattern and scheduleExpression both to a rule, however
    only through the SDK, and not through the console.

- DLQs can be configured to be used in eventbridge to assure delivery. Only standard queues can be used as DLQs for the eventbridge.

- If we want some constant thing to be sent on a scheduled basis, then we could pass that to the targets directly as input during the target setting. 


## When to use?

Functionally, SNS and Eventbridge work nearly the same. However, Eventbridge has some additional features:
- Lot more targets and 3rd party events support than SNS.
- SNS allows to filter messages based on the message attributes, but if we require content-based filtering then that has to be done in
    the code. EventBridge however supports pattern matching against the event content. Also supports others like: numeric comparison, prefix matching,
    IP address matching, etc. Thus a single event bus can suffice needs of different kinds of events, but to achieve the same in SNS, we would have to
    use multiple SNS topics.
- It has built-in schema discovery capabilities.
- Supports input transformation.