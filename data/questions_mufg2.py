"""
MUFG Global Services — Java Fullstack (JD-specific gaps)
Topics from JD: Redux/Flux, JS ES6, Prototypal Inheritance, JUnit5/Mockito,
Jest/RTL, SAML 2.0, AWS, OOP Design Patterns, GitHub Copilot AI, Agile/Scrum.
"""

_MUFG = ["MUFG Global Services"]

def A(*sections):
    parts = [f'<span class="answer-label">{l}</span><br>{c}' for l,c in sections]
    return '<div class="answer-section">'+'</div><div class="answer-section" style="margin-top:10px">'.join(parts)+'</div>'

MUFG2_Q = [

  ("mufg021","Redux state management — store, actions, reducers, middleware, Flux pattern",
   "java","reactjs","Medium",_MUFG,88,"redux,flux,store,reducer,actions,middleware,react","Technical Round",
   A(("Flux vs Redux",
      "<b>Flux</b> (Facebook pattern): Unidirectional data flow. Action → Dispatcher → Store → View → Action. "
      "Multiple stores allowed.<br>"
      "<b>Redux</b>: Evolution of Flux. Single store, pure reducer functions, time-travel debugging. "
      "Used in MUFG trade dashboards for shared state (auth, filters, trade list)."),
     ("Core Redux Concepts",
      "<pre>// 1. Action — plain object describing what happened\nconst BOOK_TRADE = 'BOOK_TRADE';\nconst bookTrade = (trade) =&gt; ({ type: BOOK_TRADE, payload: trade });\n\n// 2. Reducer — pure function: (prevState, action) =&gt; newState\nconst tradesReducer = (state = [], action) =&gt; {\n  switch (action.type) {\n    case BOOK_TRADE:\n      return [...state, action.payload];  // immutable update!\n    case 'CANCEL_TRADE':\n      return state.filter(t =&gt; t.id !== action.payload.id);\n    default:\n      return state;\n  }\n};\n\n// 3. Store — single source of truth\nimport { createStore } from 'redux';\nconst store = createStore(tradesReducer);\n\nstore.dispatch(bookTrade({ id: 'TXN-001', amount: 5000 }));\nconsole.log(store.getState());  // [{ id: 'TXN-001', amount: 5000 }]</pre>"),
     ("Modern Redux Toolkit (RTK)",
      "<pre>import { createSlice, configureStore } from '@reduxjs/toolkit';\n\nconst tradesSlice = createSlice({\n  name: 'trades',\n  initialState: { items: [], loading: false, error: null },\n  reducers: {\n    addTrade:    (state, action) =&gt; { state.items.push(action.payload); },  // Immer allows mutation!\n    cancelTrade: (state, action) =&gt; {\n      state.items = state.items.filter(t =&gt; t.id !== action.payload);\n    },\n  },\n});\n\nexport const { addTrade, cancelTrade } = tradesSlice.actions;\nconst store = configureStore({ reducer: { trades: tradesSlice.reducer } });\n\n// Async with createAsyncThunk\nimport { createAsyncThunk } from '@reduxjs/toolkit';\nexport const fetchTrades = createAsyncThunk(\n  'trades/fetchAll',\n  async () =&gt; {\n    const res = await fetch('/api/v1/trades');\n    return res.json();\n  }\n);</pre>"),
     ("Connecting to React",
      "<pre>import { useSelector, useDispatch } from 'react-redux';\n\nconst TradeDashboard = () =&gt; {\n  const trades  = useSelector(state =&gt; state.trades.items);\n  const loading = useSelector(state =&gt; state.trades.loading);\n  const dispatch = useDispatch();\n\n  useEffect(() =&gt; { dispatch(fetchTrades()); }, []);\n\n  return trades.map(t =&gt; &lt;TradeRow key={t.id} trade={t} /&gt;);\n};</pre>"),
     ("Middleware — Redux Thunk vs Saga",
      "<ul><li><b>Redux Thunk:</b> Dispatch functions (for async). Built into RTK. Simple.</li>"
      "<li><b>Redux Saga:</b> Generator-based side effects. More powerful for complex flows "
      "(retry, cancel, race conditions). Overkill for simple CRUD.</li></ul>"),
     ("Cross-Questions &amp; Follow-ups",
      '<div class="followup">• Why must reducers be pure functions? (predictable state, time-travel debugging)<br>'
      '• What is the Redux middleware chain and how does applyMiddleware work?<br>'
      '• When would you use React Context + useReducer instead of Redux?<br>'
      '• What is selector memoization (reselect library) and why does it matter for performance?<br>'
      '• How does Immer allow "mutating" state in RTK reducers safely?</div>'))),

  ("mufg022","JavaScript ES6+ — closures, promises, async/await, arrow functions, destructuring",
   "java","javascript","Medium",_MUFG,90,"javascript,es6,closures,promises,async-await,arrow-functions","Technical Round",
   A(("Closures — Most Common Interview Topic",
      "A closure is a function that <b>retains access to its outer scope</b> even after the outer function returns.<br>"
      "<pre>function makeCounter(start = 0) {\n  let count = start;  // closed-over variable\n  return {\n    increment: () =&gt; ++count,\n    decrement: () =&gt; --count,\n    value:     () =&gt; count\n  };\n}\nconst c = makeCounter(10);\nc.increment(); c.increment();\nconsole.log(c.value());  // 12\n// count is private — not accessible from outside\n\n// Classic closure pitfall (var in loop)\nfor (var i = 0; i &lt; 3; i++) {\n  setTimeout(() =&gt; console.log(i), 100);  // prints 3, 3, 3!\n}\n// Fix: use let (block scope) or IIFE\nfor (let i = 0; i &lt; 3; i++) {\n  setTimeout(() =&gt; console.log(i), 100);  // 0, 1, 2\n}</pre>"),
     ("Promises and Async/Await",
      "<pre>// Promise chain\nfetch('/api/v1/trades')\n  .then(res =&gt; {\n    if (!res.ok) throw new Error(`HTTP ${res.status}`);\n    return res.json();\n  })\n  .then(trades =&gt; setTrades(trades))\n  .catch(err =&gt; console.error('Fetch failed:', err))\n  .finally(() =&gt; setLoading(false));\n\n// async/await (syntactic sugar over Promises)\nasync function fetchTrades() {\n  try {\n    const res = await fetch('/api/v1/trades');  // suspends, doesn't block thread\n    if (!res.ok) throw new Error(`HTTP ${res.status}`);\n    return await res.json();\n  } catch (err) {\n    console.error(err);\n    throw err;  // re-throw for caller\n  }\n}\n\n// Parallel fetching\nconst [trades, books] = await Promise.all([\n  fetchTrades(),\n  fetchBooks()\n]);\n\n// First to resolve\nconst result = await Promise.race([fetchFromPrimary(), fetchFromBackup()]);</pre>"),
     ("Arrow Functions vs Regular Functions",
      "<pre>// Arrow: no own 'this', no arguments object, cannot be constructor\nconst greet = name =&gt; `Hello, ${name}`;\n\n// 'this' binding difference\nclass TradeService {\n  constructor() { this.base = '/api/v1/trades'; }\n\n  fetchRegular() {\n    return fetch(this.base)  // 'this' works\n      .then(function(res) {\n        console.log(this);  // undefined! (strict mode) or window\n        return res.json();\n      });\n  }\n\n  fetchArrow() {\n    return fetch(this.base)\n      .then(res =&gt; {\n        console.log(this);  // TradeService instance ✓\n        return res.json();\n      });\n  }\n}</pre>"),
     ("Destructuring, Spread, Rest",
      "<pre>// Destructuring\nconst { id, amount, currency = 'USD' } = trade;  // default value\nconst [first, ...rest] = trades;  // array destructuring\n\n// Spread — clone without mutation\nconst updatedTrade = { ...trade, status: 'BOOKED' };\nconst allTrades = [...existingTrades, newTrade];\n\n// Rest parameters\nconst sum = (...nums) =&gt; nums.reduce((a, b) =&gt; a + b, 0);\n\n// Template literals\nconst msg = `Trade ${id} booked for ${amount.toFixed(2)} ${currency}`;\n\n// Optional chaining + nullish coalescing\nconst bookId = trade?.book?.id ?? 'UNKNOWN';</pre>"),
     ("Cross-Questions &amp; Follow-ups",
      '<div class="followup">• What is the event loop and call stack? How does async code execute in Node.js/browser?<br>'
      '• What is the difference between == and === in JavaScript?<br>'
      '• What is hoisting? How does var vs let vs const differ?<br>'
      '• What is Promise.allSettled() and when would you use it over Promise.all()?<br>'
      '• Explain the module system: CommonJS (require/exports) vs ES Modules (import/export).</div>'))),

  ("mufg023","JavaScript prototypal inheritance — prototype chain, Object.create, class syntax",
   "java","javascript","Medium",_MUFG,82,"javascript,prototype,inheritance,object-create,class","Technical Round",
   A(("Prototype Chain",
      "Every JavaScript object has a hidden <code>[[Prototype]]</code> link. "
      "Property lookup traverses the chain until <code>null</code> is reached (Object.prototype is the top).<br>"
      "<pre>const animal = { breathe() { return 'breathing'; } };\nconst dog = Object.create(animal);  // dog's [[Prototype]] = animal\ndog.bark = function() { return 'woof'; };\n\nconsole.log(dog.bark());     // own property\nconsole.log(dog.breathe());  // found on prototype chain\nconsole.log(dog.hasOwnProperty('bark'));    // true\nconsole.log(dog.hasOwnProperty('breathe')); // false</pre>"),
     ("Constructor Function (ES5 style)",
      "<pre>function Trade(id, amount) {\n  this.id = id;\n  this.amount = amount;\n}\nTrade.prototype.format = function() {\n  return `Trade ${this.id}: ${this.amount}`;\n};\n\nconst t = new Trade('TXN-001', 5000);\nconsole.log(t.format());  // Trade TXN-001: 5000\nconsole.log(t instanceof Trade);  // true</pre>"),
     ("ES6 Class — Syntactic Sugar",
      "<pre>class Trade {\n  #amount;  // private field (ES2022)\n\n  constructor(id, amount) {\n    this.id = id;\n    this.#amount = amount;\n  }\n\n  get amount() { return this.#amount; }\n\n  format() {\n    return `Trade ${this.id}: ${this.#amount}`;\n  }\n\n  static fromJSON(json) {  // factory static method\n    return new Trade(json.id, json.amount);\n  }\n}\n\nclass BondTrade extends Trade {\n  constructor(id, amount, coupon) {\n    super(id, amount);      // must call super first\n    this.coupon = coupon;\n  }\n  format() {\n    return `${super.format()} coupon=${this.coupon}%`;\n  }\n}</pre>"),
     ("Java vs JavaScript OOP",
      "<ul><li>Java: class-based, compile-time, strongly typed</li>"
      "<li>JS: prototype-based, dynamic, weakly typed (class is syntactic sugar)</li>"
      "<li>JS has no interfaces/abstract classes natively (use duck typing or TypeScript)</li>"
      "<li><b>TypeScript</b> adds compile-time type safety to JS — used with React at MUFG</li></ul>"),
     ("Cross-Questions &amp; Follow-ups",
      '<div class="followup">• What is the difference between Object.create(null) and {}?<br>'
      '• How does new keyword work step by step? (creates object, sets prototype, calls constructor, returns)<br>'
      '• What is the difference between __proto__ and prototype?<br>'
      '• How does TypeScript interface differ from Java interface?<br>'
      '• What is mixin pattern in JavaScript and when is it preferred over inheritance?</div>'))),

  ("mufg024","JUnit 5 + Mockito — unit testing Spring Boot services (MUFG CI pipeline)",
   "java","testing","Hard",_MUFG,88,"junit5,mockito,unit-testing,spring-boot-test,mocking","Technical Round",
   A(("JUnit 5 Anatomy",
      "<pre>@ExtendWith(MockitoExtension.class)   // enables @Mock, @InjectMocks\nclass TradeBookingServiceTest {\n\n    @Mock TradeRepository tradeRepo;       // auto-created mock\n    @Mock KafkaTemplate&lt;String,Trade&gt; kafka;\n    @Mock RedisTemplate&lt;String,String&gt; redis;\n\n    @InjectMocks TradeBookingService service;  // injects mocks\n\n    @Test\n    @DisplayName(\"Book trade: idempotent — second call returns cached result\")\n    void bookTrade_idempotent() {\n        // ARRANGE\n        TradeEvent event = new TradeEvent(\"TXN-001\", BigDecimal.valueOf(5000), \"USD\");\n        String cached = \"{\\\"id\\\":\\\"TXN-001\\\",\\\"status\\\":\\\"BOOKED\\\"}\";\n        when(redis.opsForValue().get(\"TXN-001\")).thenReturn(cached);\n\n        // ACT\n        TradeResult result = service.bookTrade(event);\n\n        // ASSERT\n        assertNotNull(result);\n        assertEquals(\"BOOKED\", result.getStatus());\n        verify(tradeRepo, never()).save(any());  // DB NOT hit — cached!\n        verify(redis.opsForValue()).get(\"TXN-001\");\n    }\n\n    @Test\n    void bookTrade_newTrade_savesAndPublishes() {\n        TradeEvent event = new TradeEvent(\"TXN-002\", BigDecimal.valueOf(10000), \"GBP\");\n        when(redis.opsForValue().get(\"TXN-002\")).thenReturn(null);  // not cached\n        Trade saved = new Trade(\"TXN-002\", BigDecimal.valueOf(10000), \"GBP\", \"BOOKED\");\n        when(tradeRepo.save(any())).thenReturn(saved);\n\n        TradeResult result = service.bookTrade(event);\n\n        assertEquals(\"BOOKED\", result.getStatus());\n        verify(tradeRepo).save(any(Trade.class));\n        verify(kafka).send(eq(\"trade.booked\"), eq(\"TXN-002\"), any());\n    }\n\n    @Test\n    void bookTrade_dbFailure_throwsException() {\n        TradeEvent event = new TradeEvent(\"TXN-003\", BigDecimal.valueOf(500), \"USD\");\n        when(redis.opsForValue().get(any())).thenReturn(null);\n        when(tradeRepo.save(any())).thenThrow(new DataAccessException(\"DB down\") {});\n\n        assertThrows(TradeBookingException.class, () -&gt; service.bookTrade(event));\n        verify(kafka, never()).send(any(), any(), any()); // no publish on failure\n    }\n}</pre>"),
     ("Key Mockito Methods",
      "<ul><li><code>when(mock.method()).thenReturn(val)</code> — stub a return value</li>"
      "<li><code>when(mock.method()).thenThrow(ex)</code> — stub an exception</li>"
      "<li><code>verify(mock).method(arg)</code> — assert the method was called</li>"
      "<li><code>verify(mock, never())</code> — assert method was NEVER called</li>"
      "<li><code>verify(mock, times(2))</code> — called exactly N times</li>"
      "<li><code>any(), eq(), anyString()</code> — argument matchers</li>"
      "<li><code>ArgumentCaptor</code> — capture the argument passed to mock</li></ul>"),
     ("ArgumentCaptor Example",
      "<pre>@Test\nvoid bookTrade_capturesCorrectTradeToKafka() {\n    ArgumentCaptor&lt;Trade&gt; captor = ArgumentCaptor.forClass(Trade.class);\n    // ... arrange and act ...\n    verify(kafka).send(any(), any(), captor.capture());\n    Trade published = captor.getValue();\n    assertEquals(\"BOOKED\", published.getStatus());\n    assertEquals(\"TXN-001\", published.getId());\n}</pre>"),
     ("@SpringBootTest vs Unit Test",
      "<ul><li><code>@ExtendWith(MockitoExtension.class)</code> — pure unit test, no Spring context, fast</li>"
      "<li><code>@SpringBootTest</code> — full Spring context, slower, for integration tests</li>"
      "<li><code>@WebMvcTest(TradeController.class)</code> — slice test for controller layer only</li>"
      "<li><code>@DataJpaTest</code> — slice test for repository layer with in-memory H2</li></ul>"),
     ("Cross-Questions &amp; Follow-ups",
      '<div class="followup">• What is the difference between a mock and a stub? (stub: returns value; mock: also verifies calls)<br>'
      '• How do you test @Transactional behavior? (@DataJpaTest with rollback or @Transactional on test)<br>'
      '• What is @MockBean in Spring Boot tests vs @Mock in Mockito?<br>'
      '• How do you test exception paths with JUnit 5? (assertThrows)<br>'
      '• What is test coverage and what tool does Jenkins use? (JaCoCo, Cobertura)</div>'))),

  ("mufg025","Jest + React Testing Library — testing React components",
   "java","testing","Medium",_MUFG,84,"jest,react-testing-library,rtl,unit-test,frontend","Technical Round",
   A(("Philosophy",
      "<b>React Testing Library</b> tests components as a user would interact with them — "
      "query by text, role, label, not by CSS class or implementation detail.<br>"
      "<b>Jest</b> is the test runner (assertions, mocks, coverage)."),
     ("Component Test Example",
      "<pre>import { render, screen, fireEvent, waitFor } from '@testing-library/react';\nimport userEvent from '@testing-library/user-event';\nimport { Provider } from 'react-redux';\nimport { store } from '../store';\nimport TradeDashboard from './TradeDashboard';\n\n// Mock the API\nglobal.fetch = jest.fn();\n\ndescribe('TradeDashboard', () =&gt; {\n  beforeEach(() =&gt; {\n    fetch.mockResolvedValueOnce({\n      ok: true,\n      json: async () =&gt; [\n        { id: 'TXN-001', amount: 5000, currency: 'USD', status: 'BOOKED' },\n        { id: 'TXN-002', amount: 10000, currency: 'GBP', status: 'PENDING' },\n      ],\n    });\n  });\n\n  test('renders trade list after loading', async () =&gt; {\n    render(&lt;Provider store={store}&gt;&lt;TradeDashboard /&gt;&lt;/Provider&gt;);\n\n    // Loading state\n    expect(screen.getByText(/loading/i)).toBeInTheDocument();\n\n    // Waits for async state update\n    await waitFor(() =&gt; {\n      expect(screen.getByText('TXN-001')).toBeInTheDocument();\n      expect(screen.getByText('TXN-002')).toBeInTheDocument();\n    });\n  });\n\n  test('filters trades by search input', async () =&gt; {\n    render(&lt;Provider store={store}&gt;&lt;TradeDashboard /&gt;&lt;/Provider&gt;);\n    await waitFor(() =&gt; screen.getByText('TXN-001'));\n\n    const input = screen.getByPlaceholderText(/search/i);\n    await userEvent.type(input, 'TXN-001');\n\n    expect(screen.getByText('TXN-001')).toBeInTheDocument();\n    expect(screen.queryByText('TXN-002')).not.toBeInTheDocument();\n  });\n\n  test('shows error when fetch fails', async () =&gt; {\n    fetch.mockRejectedValueOnce(new Error('Network error'));\n    render(&lt;Provider store={store}&gt;&lt;TradeDashboard /&gt;&lt;/Provider&gt;);\n    await waitFor(() =&gt; {\n      expect(screen.getByText(/error/i)).toBeInTheDocument();\n    });\n  });\n});</pre>"),
     ("Jest Mocking",
      "<pre>// Mock a module\njest.mock('../api/tradeApi', () =&gt; ({\n  fetchTrades: jest.fn().mockResolvedValue([]),\n  bookTrade:   jest.fn().mockResolvedValue({ id: 'TXN-001', status: 'BOOKED' }),\n}));\n\n// Spy on existing function\nconst spy = jest.spyOn(tradeApi, 'fetchTrades').mockResolvedValue([]);\nexpect(spy).toHaveBeenCalledTimes(1);\n\n// Timer mocks\njest.useFakeTimers();\njest.advanceTimersByTime(5000);\njest.useRealTimers();</pre>"),
     ("Queries Priority (RTL best practice)",
      "<ol><li><code>getByRole</code> — accessible role (button, textbox, heading)</li>"
      "<li><code>getByLabelText</code> — form inputs with labels</li>"
      "<li><code>getByText</code> — visible text content</li>"
      "<li><code>getByTestId</code> — last resort (<code>data-testid</code> attr)</li></ol>"),
     ("Cross-Questions &amp; Follow-ups",
      '<div class="followup">• getByRole vs getByText vs getByTestId — when to use each?<br>'
      '• How do you test custom hooks in isolation? (renderHook from @testing-library/react)<br>'
      '• How do you handle async state in tests without hardcoded timeouts?<br>'
      '• What is snapshot testing in Jest and what are its limitations?<br>'
      '• How do you measure frontend code coverage in Jest? (--coverage flag, Istanbul)</div>'))),

  ("mufg026","SAML 2.0 authentication — SSO flow, Spring Security SAML integration",
   "security","saml","Hard",_MUFG,80,"saml,sso,idp,sp,spring-security,authentication","Technical Round",
   A(("What is SAML 2.0",
      "<b>Security Assertion Markup Language 2.0</b> — XML-based standard for Single Sign-On (SSO). "
      "Used extensively in enterprise banking for federated identity. "
      "MUFG employees authenticate once via corporate Identity Provider (ADFS/Okta) and access multiple apps.<br><br>"
      "<b>Key Actors:</b><br>"
      "<ul><li><b>Identity Provider (IdP):</b> Authenticates user, issues SAML assertion (ADFS, Okta, PingFederate)</li>"
      "<li><b>Service Provider (SP):</b> Your app (Spring Boot). Trusts IdP's assertions.</li>"
      "<li><b>Principal:</b> The end user (MUFG employee)</li></ul>"),
     ("SP-Initiated SSO Flow",
      "<pre>1. User accesses https://trade-portal.mufg.com/dashboard\n2. SP (app) detects unauthenticated → generates AuthnRequest (XML, signed)\n3. SP redirects user to IdP: https://adfs.mufg.com/saml/sso?SAMLRequest=...\n4. IdP presents login page → user enters MUFG AD credentials\n5. IdP authenticates → creates SAML Assertion XML:\n   &lt;saml:Assertion&gt;\n     &lt;saml:Subject&gt;john.doe@mufg.com&lt;/saml:Subject&gt;\n     &lt;saml:AttributeStatement&gt;\n       &lt;saml:Attribute Name=\"groups\"&gt;\n         &lt;saml:AttributeValue&gt;TRADER&lt;/saml:AttributeValue&gt;\n       &lt;/saml:Attribute&gt;\n     &lt;/saml:AttributeStatement&gt;\n     &lt;ds:Signature&gt;...XML Digital Signature...&lt;/ds:Signature&gt;\n   &lt;/saml:Assertion&gt;\n6. IdP POSTs assertion to SP ACS endpoint:\n   POST https://trade-portal.mufg.com/saml/SSO\n7. SP validates signature using IdP public certificate\n8. SP extracts user attributes, creates session → user is logged in</pre>"),
     ("Spring Security SAML (spring-security-saml2-service-provider)",
      "<pre>// application.yml\nspring.security.saml2.relyingparty:\n  registration:\n    mufg-adfs:\n      identityprovider:\n        entity-id: https://adfs.mufg.com/adfs\n        sso-url: https://adfs.mufg.com/adfs/ls/\n        verification.credentials:\n          - certificate-location: classpath:mufg-idp.crt\n      signing.credentials:\n        - private-key-location: classpath:sp-private.key\n          certificate-location: classpath:sp.crt\n\n// Security Config\n@Configuration\npublic class SecurityConfig {\n  @Bean SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {\n    return http\n        .authorizeHttpRequests(auth -&gt; auth\n            .requestMatchers(\"/public/**\").permitAll()\n            .anyRequest().authenticated())\n        .saml2Login(saml -&gt; saml\n            .loginPage(\"/saml2/authenticate/mufg-adfs\"))\n        .saml2Logout(Customizer.withDefaults())\n        .build();\n  }\n}</pre>"),
     ("SAML vs OAuth2/OIDC",
      "<ul><li><b>SAML:</b> XML-based, enterprise SSO, browser redirects, no mobile-friendly</li>"
      "<li><b>OAuth2/OIDC:</b> JSON/JWT-based, REST-friendly, mobile support, delegated authorization</li>"
      "<li>At MUFG: SAML for internal employee SSO (ADFS/Okta); OAuth2 for API-to-API and external partners</li></ul>"),
     ("Cross-Questions &amp; Follow-ups",
      '<div class="followup">• What is the difference between SAML assertion and OAuth2 access token?<br>'
      '• How do you validate a SAML assertion signature in Spring? (IdP public certificate)<br>'
      '• What is IdP-initiated vs SP-initiated SSO?<br>'
      '• How does SAML handle Single Log Out (SLO)?<br>'
      '• What is the difference between SAML 2.0 and SAML 1.1?</div>'))),

  ("mufg027","AWS services for banking — EC2, S3, RDS, Lambda, IAM, CloudWatch",
   "backend","cloud","Medium",_MUFG,82,"aws,ec2,s3,rds,lambda,iam,cloudwatch,banking","Technical Round",
   A(("Core AWS Services at MUFG",
      "<ul><li><b>EC2:</b> Virtual servers for Spring Boot microservices (or containerized via ECS/EKS)</li>"
      "<li><b>S3:</b> Object storage for trade reports, audit files, BAI2/NACHA files, static assets</li>"
      "<li><b>RDS:</b> Managed Oracle/PostgreSQL/MySQL for trade data</li>"
      "<li><b>Lambda:</b> Serverless for event-driven processing (S3 trigger → parse NACHA file → SQS)</li>"
      "<li><b>SQS:</b> Managed message queue (replace RabbitMQ for AWS-native workloads)</li>"
      "<li><b>IAM:</b> Identity and access management — roles, policies, MFA</li>"
      "<li><b>CloudWatch:</b> Logs, metrics, alarms — like Splunk but native AWS</li></ul>"),
     ("Spring Boot + AWS S3 (trade report upload)",
      "<pre>// pom.xml\n&lt;dependency&gt;\n  &lt;groupId&gt;software.amazon.awssdk&lt;/groupId&gt;\n  &lt;artifactId&gt;s3&lt;/artifactId&gt;\n  &lt;version&gt;2.21.0&lt;/version&gt;\n&lt;/dependency&gt;\n\n@Service\npublic class TradeReportUploader {\n    private final S3Client s3;\n    private final String bucket = \"mufg-trade-reports\";\n\n    public void uploadReport(String tradeDate, byte[] pdfBytes) {\n        String key = String.format(\"reports/%s/trade-report.pdf\", tradeDate);\n        s3.putObject(\n            PutObjectRequest.builder()\n                .bucket(bucket)\n                .key(key)\n                .contentType(\"application/pdf\")\n                .serverSideEncryption(ServerSideEncryption.AWS_KMS)  // encrypt at rest\n                .build(),\n            RequestBody.fromBytes(pdfBytes)\n        );\n    }\n\n    public URL generatePresignedUrl(String key) {\n        S3Presigner presigner = S3Presigner.create();\n        PresignedGetObjectRequest req = presigner.presignGetObject(r -&gt;\n            r.signatureDuration(Duration.ofMinutes(15))\n             .getObjectRequest(g -&gt; g.bucket(bucket).key(key)));\n        return req.url();\n    }\n}</pre>"),
     ("IAM Best Practices for Banking",
      "<ul><li>Principle of Least Privilege — Lambda only has S3:PutObject on specific bucket</li>"
      "<li>No hard-coded credentials — use IAM roles for EC2/Lambda, AWS Secrets Manager for DB passwords</li>"
      "<li>MFA required for IAM console access</li>"
      "<li>CloudTrail for audit: every API call logged</li>"
      "<li>Encrypt S3 with KMS-managed keys (SSE-KMS)</li>"
      "<li>VPC with private subnets for RDS — no public internet access</li></ul>"),
     ("Lambda + SQS for NACHA Processing",
      "<pre>// Triggered by SQS message (NACHA file landing in S3)\nexports.handler = async (event) =&gt; {\n  for (const record of event.Records) {\n    const { bucket, key } = JSON.parse(record.body);\n    const file = await s3.getObject({ Bucket: bucket, Key: key }).promise();\n    const transactions = parseNACHA(file.Body.toString());\n    for (const txn of transactions) {\n      await bookTransaction(txn);  // call Trade Booking Service\n    }\n  }\n};\n// Lambda scales automatically; no server management</pre>"),
     ("Cross-Questions &amp; Follow-ups",
      '<div class="followup">• How does AWS SQS differ from Kafka? When would you choose each?<br>'
      '• What is VPC peering and why is it needed between MUFG on-prem and AWS?<br>'
      '• How do you use AWS Secrets Manager in a Spring Boot app? (spring-cloud-aws)<br>'
      '• What is the difference between ECS and EKS for containerized microservices?<br>'
      '• How does CloudWatch Logs compare to Splunk for MUFG banking observability?</div>'))),

  ("mufg028","OOP Design Patterns — Factory, Strategy, Observer, Builder in Java",
   "java","design-patterns","Medium",_MUFG,86,"design-patterns,factory,strategy,observer,builder,java","Technical Round",
   A(("Factory Pattern — Object Creation",
      "Creates objects without specifying the exact class. Used in banking for creating different trade types.<br>"
      "<pre>// Abstract factory for trade validators\npublic interface TradeValidator {\n    ValidationResult validate(Trade trade);\n}\n\npublic class EquityTradeValidator implements TradeValidator {\n    public ValidationResult validate(Trade trade) {\n        // Equity-specific validation (ISIN, exchange code)\n        return validateEquityRules(trade);\n    }\n}\n\npublic class BondTradeValidator implements TradeValidator {\n    public ValidationResult validate(Trade trade) {\n        // Bond-specific (coupon rate, maturity date, credit rating)\n        return validateBondRules(trade);\n    }\n}\n\npublic class TradeValidatorFactory {\n    private static final Map&lt;String,TradeValidator&gt; validators = Map.of(\n        \"EQUITY\", new EquityTradeValidator(),\n        \"BOND\",   new BondTradeValidator(),\n        \"FX\",     new FXTradeValidator()\n    );\n\n    public static TradeValidator forType(String assetClass) {\n        return validators.computeIfAbsent(assetClass,\n            t -&gt; { throw new IllegalArgumentException(\"Unknown type: \" + t); });\n    }\n}\n// Usage: TradeValidatorFactory.forType(trade.getAssetClass()).validate(trade);</pre>"),
     ("Strategy Pattern — Interchangeable Algorithms",
      "Define family of algorithms, encapsulate each, make them interchangeable.<br>"
      "<pre>@FunctionalInterface\npublic interface FeeCalculator {\n    BigDecimal calculate(Trade trade);\n}\n\npublic class TradeService {\n    private FeeCalculator feeCalculator;  // injected\n\n    public void setFeeCalculator(FeeCalculator calc) {\n        this.feeCalculator = calc;\n    }\n\n    public BigDecimal getFee(Trade trade) {\n        return feeCalculator.calculate(trade);\n    }\n}\n\n// Different fee strategies for different clients:\nFeeCalculator retail     = t -&gt; t.getAmount().multiply(new BigDecimal(\"0.002\"));\nFeeCalculator prime      = t -&gt; t.getAmount().multiply(new BigDecimal(\"0.0005\"));\nFeeCalculator zeroFee    = t -&gt; BigDecimal.ZERO;\n\ntradeService.setFeeCalculator(prime);</pre>"),
     ("Observer Pattern — Event-Driven",
      "Subject notifies multiple observers when state changes. Basis for Spring Events and Kafka.<br>"
      "<pre>// Spring Application Events (built-in Observer)\n@Component\npublic class TradeBookingService {\n    @Autowired ApplicationEventPublisher publisher;\n\n    public Trade book(Trade trade) {\n        Trade saved = tradeRepo.save(trade);\n        publisher.publishEvent(new TradeBookedEvent(this, saved));  // notify all observers\n        return saved;\n    }\n}\n\n@Component\npublic class RiskNotifier {\n    @EventListener\n    public void onTradeBooked(TradeBookedEvent event) {\n        riskService.recalculate(event.getTrade().getBookId());\n    }\n}\n\n@Component\n@Async  // non-blocking notification\npublic class AuditLogger {\n    @EventListener\n    public void onTradeBooked(TradeBookedEvent event) {\n        auditRepo.log(event.getTrade());\n    }\n}</pre>"),
     ("Builder Pattern — Complex Object Construction",
      "<pre>// Avoid telescoping constructor anti-pattern\nTrade trade = new Trade.Builder(\"TXN-001\")\n    .amount(BigDecimal.valueOf(50000))\n    .currency(\"USD\")\n    .assetClass(\"EQUITY\")\n    .bookId(\"BOOK-EQUITY-A\")\n    .tradeDate(LocalDate.now())\n    .counterparty(\"Goldman Sachs\")\n    .build();  // validates required fields in build()\n\n// Lombok @Builder generates this automatically:\n@Builder @Getter\npublic class Trade {\n    @NonNull private final String id;\n    @NonNull private final BigDecimal amount;\n    // ...\n}</pre>"),
     ("Cross-Questions &amp; Follow-ups",
      '<div class="followup">• What is the Decorator pattern and how does Spring AOP use it?<br>'
      '• Singleton in Spring — is every @Bean a singleton? What are other scopes?<br>'
      '• What is the Chain of Responsibility pattern? How does the Spring Filter chain use it?<br>'
      '• What is the Template Method pattern and how does JdbcTemplate use it?<br>'
      '• What is the difference between Factory Method and Abstract Factory?</div>'))),

  ("mufg029","GitHub Copilot and AI-assisted development in Java + React (MUFG JD requirement)",
   "java","ai-tools","Easy",_MUFG,78,"github-copilot,ai-coding,code-generation,testing,refactoring","Technical Round",
   A(("What is GitHub Copilot",
      "AI coding assistant (OpenAI Codex / GPT-4o) integrated into VS Code, IntelliJ, Eclipse. "
      "Generates code suggestions from natural language comments and existing context. "
      "MUFG JD requires: experience using Copilot for Java, Spring Boot, and React development."),
     ("Copilot for Java / Spring Boot",
      "<pre>// 1. Code Generation — type a comment and Copilot suggests the implementation\n// Write a Spring Boot REST endpoint to book a trade with idempotency key\n@PostMapping\npublic ResponseEntity&lt;TradeDto&gt; bookTrade(\n        @RequestBody @Valid BookTradeRequest req,\n        @RequestHeader(\"Idempotency-Key\") String key) {\n    return ResponseEntity.status(201).body(tradeService.book(req, key));\n}\n\n// 2. Test Generation — Copilot generates JUnit tests\n// Write a JUnit 5 test for TradeBookingService.bookTrade with Mockito\n@Test\nvoid bookTrade_newTrade_savesAndPublishesToKafka() { ... }\n\n// 3. Refactoring — ask Copilot Chat\n// \"Refactor this method to use Stream API instead of for-loop\"\n// \"Add proper error handling and logging\"\n\n// 4. Documentation — auto-generate Javadoc\n/**\n * Books a trade with idempotency guarantee.\n * @param request Trade booking details\n * @param idempotencyKey Unique client-generated key to prevent duplicate bookings\n * @return Booked trade DTO\n * @throws TradeNotFoundException if referenced entities don't exist\n */</pre>"),
     ("Copilot for React / JavaScript",
      "<pre>// Type a comment and get full component suggestions:\n// Create a React hook to fetch trades from /api/v1/trades with loading and error states\nexport const useTrades = () =&gt; {\n  const [trades, setTrades] = useState([]);\n  const [loading, setLoading] = useState(true);\n  const [error, setError] = useState(null);\n\n  useEffect(() =&gt; {\n    fetch('/api/v1/trades')\n      .then(r =&gt; { if(!r.ok) throw new Error(r.status); return r.json(); })\n      .then(setTrades)\n      .catch(setError)\n      .finally(() =&gt; setLoading(false));\n  }, []);\n\n  return { trades, loading, error };\n};</pre>"),
     ("Responsible AI — Security and Code Review",
      "MUFG JD emphasizes: <b>review, secure, and optimize AI-generated code</b>.<br>"
      "<ul><li>Never commit Copilot code without review — it may introduce SQL injection, XSS, weak crypto</li>"
      "<li>Copilot may suggest deprecated APIs or outdated patterns</li>"
      "<li>Verify generated code against Veracode SAST scan — Copilot doesn't guarantee security</li>"
      "<li>PII/sensitive data must not be pasted into Copilot (data leakage risk)</li>"
      "<li>IP concerns: Copilot may reproduce copyrighted code — use with caution in banking</li></ul>"),
     ("AI Across the SDLC",
      "<ul><li><b>Planning:</b> Copilot Chat for story decomposition, API design discussions</li>"
      "<li><b>Coding:</b> Code completion, boilerplate generation (DTOs, mappers, validators)</li>"
      "<li><b>Testing:</b> JUnit/Jest test generation from method signatures</li>"
      "<li><b>Debugging:</b> Explain error messages, suggest fixes</li>"
      "<li><b>Documentation:</b> Generate Javadoc, API docs, README</li></ul>"),
     ("Cross-Questions &amp; Follow-ups",
      '<div class="followup">• How do you evaluate the quality of Copilot-generated code before merging?<br>'
      '• What are the data privacy risks of using AI coding tools with banking code?<br>'
      '• How does Copilot differ from ChatGPT for coding tasks?<br>'
      '• What is RAG (Retrieval-Augmented Generation) and could it be used for internal MUFG code assistance?<br>'
      '• How do you ensure AI-generated tests actually test the right behavior?</div>'))),

  ("mufg030","Agile/Scrum for banking delivery — sprints, ceremonies, definition of done",
   "behavioral","agile","Easy",_MUFG,80,"agile,scrum,sprint,ceremonies,banking","HR Round",
   A(("Scrum Framework at MUFG",
      "<b>Roles:</b> Product Owner (PO), Scrum Master, Development Team (you)<br><br>"
      "<b>Events (Ceremonies):</b><br>"
      "<ul><li><b>Sprint Planning (start of sprint):</b> Team pulls stories from backlog into sprint. "
      "Estimates via story points (Fibonacci: 1,2,3,5,8,13). Agree on sprint goal.</li>"
      "<li><b>Daily Standup (15 min):</b> What did I do? What will I do? Any blockers?</li>"
      "<li><b>Sprint Review (end of sprint):</b> Demo completed features to stakeholders</li>"
      "<li><b>Sprint Retrospective:</b> What went well? What to improve? Action items.</li>"
      "<li><b>Backlog Refinement (mid-sprint):</b> Groom future stories, clarify ACs, estimate</li></ul>"),
     ("Definition of Done (DoD) in Banking",
      "A story is DONE only when:<br>"
      "<ol><li>Code complete + peer reviewed (PR approved)</li>"
      "<li>Unit tests written (>80% coverage via JaCoCo)</li>"
      "<li>Integration tests pass</li>"
      "<li>Veracode SAST scan — no P1/P2 findings</li>"
      "<li>Jenkins pipeline green (build + test + scan + deploy to UAT)</li>"
      "<li>Functional testing in UAT signed off by QA</li>"
      "<li>No known critical bugs</li>"
      "<li>API documentation updated (Swagger/OpenAPI)</li></ol>"),
     ("User Story Format at MUFG",
      "<pre>Title: As a Trader, I want to book an equity trade via REST API\n\nAcceptance Criteria (Gherkin):\nGiven: I have a valid trade payload with idempotency key\nWhen: I POST to /api/v1/trades\nThen: Trade is created with status=BOOKED\nAnd: Trade is published to Kafka trade.booked topic\nAnd: HTTP 201 Created is returned with trade ID\n\nNon-functional:\n- Response time &lt; 200ms p99\n- Idempotent: same key returns same result without re-processing</pre>"),
     ("Handling Banking-Specific Constraints in Agile",
      "<ul><li><b>Regulatory releases:</b> Fixed deadlines (MIFID II reporting, Volcker rule compliance)</li>"
      "<li><b>Change Management:</b> All prod deployments need CAB approval — plan release windows</li>"
      "<li><b>Risk gates:</b> Security review and Veracode scan mandatory before go-live</li>"
      "<li><b>Audit trails:</b> Every story must generate traceable audit log entries</li></ul>"),
     ("Cross-Questions &amp; Follow-ups",
      '<div class="followup">• What is velocity and how do you use it for sprint planning?<br>'
      '• How do you handle a story that won\'t fit in a sprint? (spike → break down)<br>'
      '• Scrum vs Kanban — when would MUFG use Kanban?<br>'
      '• How do you manage technical debt in banking systems where feature delivery pressure is high?<br>'
      '• What is a release train (SAFe) and do large banks like MUFG use it?</div>'))),

  ("mufg031","Spring Boot + React full-stack integration — API calls, CORS, JWT auth flow",
   "java","fullstack","Hard",_MUFG,86,"spring-boot,react,cors,jwt,fullstack,integration","Technical Round",
   A(("Full-Stack Architecture at MUFG",
      "<pre>React SPA (port 3000 in dev, Nginx in prod)\n      |\n    HTTPS + JWT Bearer token\n      |\n Spring Boot API (port 8080) ← CORS configured\n      |\n    Oracle DB | Kafka | Redis</pre>"),
     ("CORS Configuration in Spring Boot",
      "<pre>@Configuration\npublic class CorsConfig {\n    @Bean\n    public CorsConfigurationSource corsConfigurationSource() {\n        CorsConfiguration config = new CorsConfiguration();\n        config.setAllowedOrigins(List.of(\n            \"https://trade-portal.mufg.com\",\n            \"http://localhost:3000\"   // dev only\n        ));\n        config.setAllowedMethods(List.of(\"GET\",\"POST\",\"PUT\",\"PATCH\",\"DELETE\",\"OPTIONS\"));\n        config.setAllowedHeaders(List.of(\"Authorization\",\"Content-Type\",\"Idempotency-Key\"));\n        config.setAllowCredentials(true);\n        config.setMaxAge(3600L);\n\n        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();\n        source.registerCorsConfiguration(\"/api/**\", config);\n        return source;\n    }\n}</pre>"),
     ("JWT Auth Flow (React → Spring Boot)",
      "<pre>// React: login and store token\nasync function login(username, password) {\n  const res = await fetch('/api/auth/login', {\n    method: 'POST',\n    headers: { 'Content-Type': 'application/json' },\n    body: JSON.stringify({ username, password })\n  });\n  const { accessToken, refreshToken } = await res.json();\n  // Store accessToken in memory (NOT localStorage - XSS risk)\n  // Store refreshToken in HttpOnly cookie (set by server)\n  tokenStore.setAccessToken(accessToken);\n}\n\n// React: Axios interceptor to attach token\naxios.interceptors.request.use(config =&gt; {\n  const token = tokenStore.getAccessToken();\n  if (token) config.headers.Authorization = `Bearer ${token}`;\n  return config;\n});\n\n// React: Refresh token on 401\naxios.interceptors.response.use(\n  res =&gt; res,\n  async err =&gt; {\n    if (err.response?.status === 401) {\n      const newToken = await refreshAccessToken();\n      err.config.headers.Authorization = `Bearer ${newToken}`;\n      return axios(err.config);  // retry original request\n    }\n    return Promise.reject(err);\n  }\n);</pre>"),
     ("OpenAPI/Swagger for React Integration",
      "<pre>// Spring Boot: generate OpenAPI docs\n// pom.xml: springdoc-openapi-starter-webmvc-ui\n// Access: http://localhost:8080/swagger-ui.html\n\n// React: use openapi-typescript-codegen to generate typed API client\n// npx openapi-typescript-codegen --input http://localhost:8080/api-docs \\\n//   --output src/api --client fetch\n// Result: type-safe TradeApiClient.bookTrade(request) — no manual fetch!</pre>"),
     ("Cross-Questions &amp; Follow-ups",
      '<div class="followup">• What is a preflight OPTIONS request and why does it happen?<br>'
      '• How do you handle file uploads from React to Spring Boot (multipart/form-data)?<br>'
      '• What is the difference between session cookies and JWT for auth in SPAs?<br>'
      '• How do you proxy API calls in Create React App dev server? (proxy in package.json)<br>'
      '• How would you implement role-based UI rendering in React? (conditional rendering based on JWT claims)</div>'))),

]

def _to_dict(q):
    return {"id":q[0],"text":q[1],"category":q[2],"subcategory":q[3],"difficulty":q[4],
            "companies":q[5],"frequency":q[6],"tags":q[7].split(","),"round_type":q[8],"answer_hint":q[9]}

QUESTIONS = [_to_dict(q) for q in MUFG2_Q]
