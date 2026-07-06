# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
1) The program is supposed to create a daily plan/schedule for pet owners to keep up with their responsibilities pertaining to their pet. The program should take in the owners' schedule and basic info, the pets basic info and needs, and how long each task will take. 
- What classes did you include, and what responsibilities did you assign to each?
1)  The classes I would include are: Owner, Pet, Task, Scheduler. The Owner class would hold the personal info of the owner, so their name, birthday, number, and email. The Pet class would hold the info on the pets, so their name, birthday, kind of animal it is, what medication it's on (if it's on any), and how often it needs to eat. The Task class would hold each task as it's own objects. The Scheduler would hold the owner's schedule and how often the pet gets groomed (if it gets groomed), and how often their pet has to be taken outside.
2) The methods I would put in each class:
Owner: initializers that take in name, birthday, email and number, get and set methods for name, birthday, email and number. 
Pet: initializer for name, birthday, animal type, and feeding frequency,  get and set methods for name, birthday, animal type, and feeding frequency
Task: initalizers that create new tasks and set their priority level, get and set method to create tasks and their priority level, methods that add and remove tasks to a list, with each day being a new list, also a methods that add and remove tasks from a list for monthly tasks 
Scheduler: initializer to create a new schedule, a method that would organize the schedule based on date, a method that organizes the schedule based on priority level 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
