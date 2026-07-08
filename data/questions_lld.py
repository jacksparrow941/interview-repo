"""
LLD (Low-Level Design / Machine Coding) and Behavioral questions.
Added as a separate module to keep file sizes manageable.
"""

_G2 = ["Google","Meta","Amazon"]
_G3 = ["Google","Meta","Amazon","Microsoft","Uber","LinkedIn"]
_IND = ["Razorpay","PhonePe","Swiggy","Zomato","CRED","Dream11","Groww"]

LLD_QUESTIONS = [
  # id, text, cat, sub, diff, companies, freq, tags, round, hint
  ("lld001","Design a Parking Lot System","lld","machine_coding","Medium",_G2+["Microsoft","Uber","Adobe","Razorpay"],88,"oop,design-patterns,state-machine","LLD Round","Entities: ParkingLot, Floor, Spot, Vehicle, Ticket, Payment. Strategy pattern for pricing. Observer for display."),
  ("lld002","Design a Library Management System","lld","machine_coding","Medium",_G2+["Microsoft","Adobe","Amazon","LinkedIn"],82,"oop,design-patterns","LLD Round","Entities: Library, Book, Member, Librarian, Loan. Observer for due-date alerts. Factory for book types."),
  ("lld003","Design an ATM Machine","lld","machine_coding","Medium",_G2+["PayPal","Stripe","Razorpay","PhonePe"],85,"state-machine,oop","LLD Round","State machine: Idle→CardInserted→AuthenticatingPIN→ChoosingAction→Dispensing→EjectingCard. Finite state pattern."),
  ("lld004","Design a Hotel Booking System","lld","machine_coding","Medium",["Google","Airbnb","Amazon","LinkedIn","Expedia"],83,"oop,decorator,strategy","LLD Round","Entities: Hotel, Room, Booking, Guest, Payment. Strategy for pricing (seasonal). Observer for availability."),
  ("lld005","Design a Ride-Sharing App (Uber/Ola)","lld","machine_coding","Hard",["Uber","Google","Swiggy","Ola","Razorpay"],90,"state-machine,observer,strategy","LLD Round","Driver/Rider entities, Trip state machine: Requested→Accepted→Arrived→InProgress→Completed. Observer for notifications."),
  ("lld006","Design an Elevator System","lld","machine_coding","Medium",_G2+["Microsoft","Amazon","Adobe"],85,"design-patterns,scheduler","LLD Round","Entities: ElevatorSystem, Elevator, Floor, Request. Scheduling strategies: SCAN, LOOK, SSTF. State per elevator."),
  ("lld007","Design a Chess Game","lld","machine_coding","Hard",_G2+["Microsoft","Apple","Adobe"],80,"oop,strategy","LLD Round","Piece hierarchy (King/Queen/Rook/Bishop/Knight/Pawn). Board, Player, Game, Move. Each piece has valid_moves()."),
  ("lld008","Design a Snake and Ladder Game","lld","machine_coding","Easy",["Amazon","Microsoft","Adobe","TCS","Infosys"],78,"oop,simulation","LLD Round","Board, Player, Dice, Snake, Ladder entities. Turn-based simulation. Simple to extend with special cells."),
  ("lld009","Design a Vending Machine","lld","machine_coding","Medium",_G2+["Microsoft","Oracle","Cisco"],82,"state-machine,design-patterns","LLD Round","States: Idle→HasMoney→SelectProduct→Dispensing→GiveChange. Strategy for payment. State pattern."),
  ("lld010","Design a Movie Ticket Booking System (BookMyShow)","lld","machine_coding","Hard",["Amazon","Swiggy","Zomato","PhonePe","Razorpay","CRED"],88,"oop,concurrency,lock","LLD Round","Entities: Theatre, Screen, Show, Seat, Booking, Payment. Optimistic locking for seat reservation. Payment saga."),
  ("lld011","Design a Food Delivery System","lld","machine_coding","Hard",["Swiggy","Zomato","Uber","Amazon","CRED"],85,"oop,observer,strategy","LLD Round","Restaurant, Menu, Order, Delivery Agent, Customer. Observer for order status. Strategy for delivery assignment."),
  ("lld012","Design an Online Shopping Cart","lld","machine_coding","Medium",["Amazon","Flipkart","Walmart","Meesho","Razorpay"],83,"oop,strategy,decorator","LLD Round","Cart, Item, Discount (Strategy), Payment (Strategy). Decorator for promotions. Singleton CartManager."),
  ("lld013","Design a Notification System","lld","machine_coding","Medium",_G3[:5]+["Razorpay","CRED","PhonePe"],86,"observer,factory,chain-of-responsibility","LLD Round","Observer pattern: Subject→Observers (Email/SMS/Push). Factory for channel creation. Chain for fallback routing."),
  ("lld014","Design a Cache (LRU / LFU)","lld","machine_coding","Hard",_G3[:5]+["Razorpay","Databricks"],90,"design-patterns,doubly-linked-list","LLD Round","LRU: HashMap + DLL. LFU: 2 HashMaps. Generic Cache<K,V> with pluggable eviction strategy (Strategy pattern)."),
  ("lld015","Design a Logger Framework","lld","machine_coding","Medium",_G3[:5]+["Adobe","Atlassian"],82,"chain-of-responsibility,singleton,observer","LLD Round","Log levels (DEBUG/INFO/WARN/ERROR). Chain of Responsibility for handlers. Appenders (File/Console/Remote). Async logging."),
  ("lld016","Design a Rate Limiter (code-level)","lld","machine_coding","Hard",["Stripe","Google","Uber","Razorpay","CRED"],88,"token-bucket,sliding-window,concurrent","LLD Round","Token Bucket: AtomicLong tokens, scheduled refill. Thread-safe. RateLimiter<K> with per-key limits."),
  ("lld017","Design an Event Bus / Pub-Sub System","lld","machine_coding","Medium",_G3[:5]+["Razorpay","LinkedIn"],82,"observer,generics,concurrent","LLD Round","EventBus with topic→List<Subscriber>. Async dispatch with ExecutorService. Type-safe via generics."),
  ("lld018","Design a File System","lld","machine_coding","Hard",["Google","Meta","Apple","Dropbox","Microsoft"],80,"composite,oop","LLD Round","Composite pattern: FileSystemNode→File|Directory. Directory contains children. Operations: create/delete/search/size."),
  ("lld019","Design a Traffic Light System","lld","machine_coding","Medium",["Cisco","Google","Uber","Amazon"],75,"state-machine,observer","LLD Round","State machine per light: Red→Green→Yellow→Red. Timer triggers transitions. Observer notifies connected intersections."),
  ("lld020","Design a Cricket Score Tracker","lld","machine_coding","Medium",["Dream11","Amazon","Microsoft","TCS","Infosys"],80,"oop,observer","LLD Round","Match, Innings, Over, Ball, Batsman, Bowler entities. Observer for scorecard updates. Strategy for DLS method."),
  ("lld021","Design a URL Shortener (code-level)","lld","machine_coding","Medium",_G3[:5]+["Razorpay","PhonePe"],85,"hashing,concurrent","LLD Round","Base62 encoding. ConcurrentHashMap<shortCode, URL>. Thread-safe counter. Expiry with ScheduledExecutor."),
  ("lld022","Design a Concurrent Task Scheduler","lld","machine_coding","Hard",_G3[:4]+["Stripe","Razorpay"],82,"concurrent,priority-queue,thread-pool","LLD Round","PriorityQueue<Task> by schedule time. ScheduledThreadPoolExecutor. Retry logic. Task states: PENDING/RUNNING/DONE/FAILED."),
  ("lld023","Design a Leaderboard System","lld","machine_coding","Medium",["Dream11","Google","Amazon","CRED","Zomato"],82,"sorted-set,concurrent","LLD Round","TreeMap or Redis sorted set for O(log n) rank. ConcurrentSkipListMap for lock-free. Paginated top-K queries."),
  ("lld024","Design a Key-Value Store","lld","machine_coding","Hard",["Google","Meta","Amazon","Databricks","Snowflake"],83,"lsm-tree,wal,concurrent","LLD Round","In-memory: ConcurrentHashMap. Persistence: WAL + SSTable. Compaction thread. CRUD + TTL support."),
  ("lld025","Design a Connection Pool","lld","machine_coding","Hard",["Google","Meta","Amazon","Stripe","Razorpay"],80,"blocking-queue,semaphore,concurrent","LLD Round","BlockingQueue of connections. Borrow/return with timeout. Health check thread. Max size, idle timeout."),
]

BEHAVIORAL_QUESTIONS = [
  ("beh001","Tell me about a time you handled a production incident","behavioral","conflict","Medium",_G2+["Amazon","Uber","LinkedIn","Stripe","Razorpay","CRED"],88,"incident,ownership,reliability","Behavioral Round","STAR format. Emphasize: detection (monitoring), diagnosis (logs/traces), mitigation, RCA, prevention."),
  ("beh002","Describe a technical disagreement and how you resolved it","behavioral","conflict","Medium",_G3+["Razorpay","Swiggy","PhonePe"],84,"conflict-resolution,communication","Behavioral Round","Show data-driven approach, active listening, willingness to change your mind when shown evidence."),
  ("beh003","Tell me about the most complex system you designed","behavioral","design","Hard",_G3+_IND,86,"system-design,complexity,scale","Behavioral Round","Use STAR. Focus on scale challenges, trade-offs made, alternatives considered, outcome metrics."),
  ("beh004","Describe a time you had to learn a new technology quickly","behavioral","growth","Medium",_G3+_IND,82,"learning,adaptability","Behavioral Round","Show initiative, structured learning approach, how you applied it, and what you'd do differently."),
  ("beh005","How do you handle competing priorities and tight deadlines?","behavioral","planning","Medium",["Amazon","Google","Meta","Uber","LinkedIn","Razorpay","Swiggy"],84,"prioritization,time-management","Behavioral Round","Communicate early, use impact vs effort matrix, negotiate scope, keep stakeholders informed."),
  ("beh006","Tell me about a time you improved a team's engineering process","behavioral","leadership","Medium",_G3+_IND,80,"leadership,process-improvement","Behavioral Round","Show initiative. Metrics before/after. Got buy-in. Made it stick with documentation and ownership."),
  ("beh007","Describe your biggest technical failure and what you learned","behavioral","failure","Medium",_G3+_IND,85,"ownership,learning","Behavioral Round","Honesty and depth of analysis matters more than the failure itself. Show systematic prevention."),
  ("beh008","Amazon Leadership Principles: Customer Obsession example","behavioral","amazon_lp","Medium",["Amazon"],88,"amazon-lp,customer","Behavioral Round","Specific example of going beyond requirements to serve customer. Measurable impact. Own the outcome."),
  ("beh009","Amazon LP: Dive Deep — technical investigation example","behavioral","amazon_lp","Medium",["Amazon"],85,"amazon-lp,dive-deep","Behavioral Round","Data-driven investigation, root cause analysis, preventing recurrence. Metrics and specifics."),
  ("beh010","Amazon LP: Ownership — took responsibility beyond your role","behavioral","amazon_lp","Medium",["Amazon"],86,"amazon-lp,ownership","Behavioral Round","Show stepping up without being asked. Long-term thinking. Driving to completion despite obstacles."),
]

from data.questions_coding import QUESTIONS as CODING_Q
from data.questions_other import (BACKEND_QUESTIONS, CPP_QUESTIONS, JAVA_QUESTIONS,
                                   GO_QUESTIONS, SYSDESIGN_QUESTIONS, DB_QUESTIONS,
                                   OS_QUESTIONS, NET_QUESTIONS, CONC_QUESTIONS)

def _to_dict(q):
    return {
        "id": q[0], "text": q[1], "category": q[2], "subcategory": q[3],
        "difficulty": q[4], "companies": q[5], "frequency": q[6],
        "tags": q[7].split(","), "round_type": q[8], "answer_hint": q[9]
    }

LLD_Q = [_to_dict(q) for q in LLD_QUESTIONS]
BEHAVIORAL_Q = [_to_dict(q) for q in BEHAVIORAL_QUESTIONS]

ALL_QUESTIONS_EXTENDED = (
    CODING_Q +
    [_to_dict(q) for q in (BACKEND_QUESTIONS + CPP_QUESTIONS + JAVA_QUESTIONS +
                            GO_QUESTIONS + SYSDESIGN_QUESTIONS + DB_QUESTIONS +
                            OS_QUESTIONS + NET_QUESTIONS + CONC_QUESTIONS)] +
    LLD_Q +
    BEHAVIORAL_Q
)
