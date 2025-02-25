import streamlit as st
import time

# Custom CSS styling
st.markdown("""
<style>
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg,#6FFFB0,#7D4EFF,#FF7D7D,#FFD700);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        min-height: 100vh;
    }

    .question-box {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }

    .score-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(5px);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(99, 214, 235, 0.1);
    }

    .header-text {
        color: white!important;
        font-size: 3.5rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        text-align: center;
        margin-bottom: 2rem !important;
    }

    /* Chat Interface Styles */
    .chat-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 999;
        background:rgb(115, 163, 245);
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }

    .chat-container {
        position: fixed;
        bottom: 100px;
        right: 30px;
        width: 350px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        max-height: 60vh;
        display: none;
    }

    .chat-visible {
        display: flex;
        flex-direction: column;
    }

    .chat-header {
        background: #1F63DA;
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 0 0;
        font-weight: bold;
    }

    .chat-messages {
        flex-grow: 1;
        overflow-y: auto;
        padding: 1rem;
    }

    .message {
        margin: 0.5rem 0;
        padding: 0.8rem 1rem;
        border-radius: 15px;
        max-width: 80%;
        animation: fadeIn 0.3s ease;
    }

    .user-message {
        background: #1F63DA;
        color: white;
        margin-left: auto;
    }

    .bot-message {
        background: #48BB78;
        color: white;
        margin-right: auto;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .completion-screen {
        background: rgba(145, 240, 247, 0.9);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 2rem auto;
        max-width: 600px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_day' not in st.session_state:
    st.session_state.update({
        'current_day': 1,
        'score': 0,
        'answers': {},
        'show_explanations': False,
        'chat_visible': False,
        'chat_history': []
    })


# Question bank
QUESTIONS = {
    1: {
        "technology": "HTML",
        "questions": [
            {
                "question": "Which tag is used for main content?",
                "options": [ "<content>","<main>", "<body>", "<div>"],
                "answer": 1,
                "explanation": "The main tag specifies the main content of a document."
            },
            {
                "question": "Which attribute makes an email input field required?",
                "options": ["required=\"true\"", "validate=\"email\"", "required", "type=\"mandatory\""],
                "answer": 2,
                "explanation": "The boolean 'required' attribute enforces validation."
            },
            {
                "question": "How to group related form elements?",
                "options": ["<group>", "<form-group>", "<fieldset>",  "<div class=group>"],
                "answer": 2,
                "explanation": "A fieldset groups form controls with a <legend>."
            },
            {
                "question": "What does the alt attribute do in <img>?",
                "options": [ " Links to another image", " Sets alignment","Adds a border","Provides alternative text"],
                "answer": 3,
                "explanation": "The alt attribute provides alternative text for an image."
            },
            {
                 "question": "What is the correct table structure?",
                "options": ["<table><row><cell></cell></row></table>", " <table><tr><td></td></tr></table>", "<table><thead><tdata></tdata></thead></table>","<table><th><tr></tr></th></table>"],
                "answer": 1,
                "explanation": "tr = table row, td = table data."
            },
            {
                 "question": "How to create a dropdown list?",
                "options": ["<input type='dropdown'>", " <list>", " <select>","<datalist>"],
                "answer": 2,
                "explanation": " select with option tags."
            },
            {
                 "question": "How to write © symbol in HTML?",
                "options": ["&copy;", "&#169;", "Both a and b","<copyright>"],
                "answer": 2,
                "explanation": "Both &copy; and &#169; work."
            },
            {
                 "question": "What’s the difference between id and class?",
                "options": [ " `class` uses # in CSS", "`id` is for styling only","`id` is unique, `class` can be reused"," No difference"],
                "answer": 2,
                "explanation": "id must be unique, class is reusable."
            },
            
            {
                 "question": "What does <iframe> do?",
                "options": ["Embeds another webpage", "Creates a frame", "Adds a border","Loads a script"],
                "answer": 0,
                "explanation": "Embeds external content like maps/videos."
            },
            {
                 "question": "Which is an inline element?",
                "options": [" <div>", " <p>", "<span>","<section>"],
                "answer": 2,
                "explanation": "Inline elements don’t start new lines."
            },
        ]
    
    },
    2: {
        "technology": "CSS",
        "questions": [
            {
                "question": "Which property controls space between elements?",
                "options": ["padding", "margin", "gap", "spacing"],
                "answer": 1,
                "explanation": "margin controls space outside elements."
            },
            {
                "question": "Which property controls the space inside an element?",
                "options": ["margin", "padding", "gap", "spacing"],
                "answer": 1,
                "explanation": "Padding creates space between the element's content and its border."
            },
            {
                "question": "What does position: absolute do?",
                "options": ["Positions relative to viewport  ", " Positions relative to parent ", "Positions relative to normal flow", " Positions relative to sibling  "],
                "answer": 1,
                "explanation": "Absolute positioning removes the element from normal flow."
            },
            {
                "question": "Which selector has highest specificity?",
                "options": [" .class" ,   "#id", " tag ", " inline style "],
                "answer": 3,
                "explanation": "Specificity order: inline > ID > class > tag."
            },
            {
                "question": "How to center an element horizontally?",
                "options": [" margin: 0 auto;" ,   "text-align: center;", " align-items: center ", " position: center; "],
                "answer": 0,
                "explanation": "Requires width and display: block."
            },
            {
                "question": "What does z-index control?",
                "options": ["Font size", "Stacking order  ", "Color depth ", "Animation speed"],
                "answer": 1,
                "explanation": "Works with positioned elements (relative/absolute/fixed)."
            },
            {
                "question": " Which is NOT a valid CSS unit?",
                "options": ["rem   ", "vh  ", "px ", " dpi  "],
                "answer": 3,
                "explanation": "Valid units include rem, vh, px, em, %, etc."
            },
            {
                "question": "How to hide an element visually?",
                "options": ["display: none;  ", "visibility: hidden;", "opacity: 0;  ", " All of the above "],
                "answer": 3,
                "explanation": "Different methods with varying behavior."
            },
            {
                "question": "Which media query targets mobile screens?",
                "options": ["@media (min-width: 768px) ", " @media (max-width: 480px)  ", " @media (orientation: portrait)  ", "@media (color)  "],
                "answer": 1,
                "explanation": "Common mobile breakpoint."
            },
            {
                "question": "What does grid-template-columns: 1fr 2fr create?",
                "options": [" 2 equal columns  ", "1 fixed + 2 fluid columns  ", " Ratio-based columns (1:2) ", "3 columns "],
                "answer": 2,
                "explanation": "fr = fractional unit."
            },
        ]
    },
    3: {
        "technology": "JAVA SCRIPT",
        "questions": [
            {
                "question": " What is the output of typeof null?",
                "options": ["object"  ,"null","undefined","NaN"],
                "answer": 1,
                "explanation": "This is a known JavaScript quirk. Use === null to check for null."
            },
            {
                "question": " Which is NOT a JavaScript framework?",
                "options": ["React "  ,"Angular","Django ","Vue  "],
                "answer": 2,
                "explanation": "Django is a Python framework."
            },
            {
                "question": " Which method deep-copies an object?",
                "options": [" Object.assign() "  ," JSON.parse(JSON.stringify(obj)) ","Spread operator  ","All of the above "],
                "answer": 1,
                "explanation": " Only this method handles nested objects fully."
            },
            {
                "question": " What does let have that var doesn’t?",
                "options": [" Block scope  "  ," Global scope","Hoisting  ","Reassignment  "],
                "answer": 0,
                "explanation": "let and const are block-scoped, var is function-scoped."
            },
            {
                "question": " What is a closure?",
                "options": ["A function inside another function  "  ,"A function with access to its outer scope "," A callback function ","An IIFE  "],
                "answer": 1,
                "explanation": "Closures preserve the outer function’s variables."
            },
            {
                "question": " How is typeof NaN evaluated?  " ,
                "options": ["undefined"  ,"NaN","number","string"],
                "answer": 2,
                "explanation": "NaN (Not a Number) is still of type number in JavaScript.typeof NaN returns 'number', even though it means an invalid number."
            },
            {
                "question": " Which method adds an element to an array’s end?",
                "options": ["  pop()  "  ," push() ","shift()  "  ,"  unshift()   "],
                "answer": 1,
                "explanation": "push() appends, pop() removes from the end."
            },
            {
                "question": " What does use strict do?",
                "options": [" Removes type coercion     "  ,"Disables hoisting  ","Allows global variables  ","Enables strict mode   "],
                "answer": 3,
                "explanation": "Catches silent errors and prevents unsafe actions."
            },
            {
                "question": " What is the event loop responsible for?",
                "options": ["  Executing synchronous code   "  ,"Handling asynchronous callbacks  ","Memory management   ","DOM rendering    "],
                "answer": 1,
                "explanation": "Manages the callback queue and call stack."
            },
            {
                "question": "  What is the output?   const arr = [1, 2, 3];  console.log(arr[5]);  ",
                "options": [" Error "  ," 5","null  ","undefined    "],
                "answer": 3,
                "explanation": "JavaScript returns undefined for out-of-bound indices."
            },
            ]
    },
            4: {
        "technology": "TYPE SCRIPT",
        "questions": [
            {
                "question": "What is TypeScript primarily used for?",
                "options": ["Adding dynamic typing to JavaScript"  ,"Adding static typing to JavaScript","Replacing JavaScript entirely","Simplifying CSS"],
                "answer": 1,
                "explanation": "TypeScript extends JavaScript with optional static type-checking."
            },
            {
                "question": " Which keyword defines a custom type for an object shape?",
                "options": ["interface "  ,"type","class ","Both a and b  "],
                "answer": 3,
                "explanation": " Both type and interface can define object shapes, but interface is more extendable."
            },
            {
                "question": "Which type in TypeScript represents the absence of a value?  ",
                "options": ["null "  ,"undefined","Error ","void  "],
                "answer": 3,
                "explanation": "void is used when a function does not return anything."
            },
            {
                "question": "  How to define an array of strings in TypeScript?",
                "options": ["let arr: string[] = [] "  ," let arr: array<string> = []","let arr: Array<string> = [] ","All of the above  "],
                "answer": 3,
                "explanation": "string[] and Array<string> are valid."
            },
            {
                "question": " . What does the readonly keyword do?",
                "options": ["Prevents object mutation "  ," Makes a property immutable","Restricts variable reassignment "," Both b and c  "],
                "answer": 1,
                "explanation": "readonly ensures a property cannot be modified after initialization."
            },
            {
                "question": " Which is a valid enum declaration?",
                "options": [" enum Status { Active, Inactive } "  ,"enum Status { 'Active', 'Inactive' }", "const enum Status = { Active, Inactive }","enum Status = ['Active', 'Inactive']  "],
                "answer": 0,
                "explanation": "Enums use curly braces and PascalCase by convention."
            },
            {
                "question": " What is the difference between any and unknown?",
                "options": [" unknown allows any operations; any requires type checks"  ," They are interchangeable","any allows any operations; unknown requires type checks ","unknown is deprecated  "],
                "answer": 2,
                "explanation": "unknown is safer and requires type assertion/narrowing."
            },
            {
                "question": "  How to define a generic function?",
                "options": [" function identity<T>(arg: any): any { ... }"  ,"function identity<T>(arg: T): T { ... }","function identity(arg: generic): generic { ... } ","function identity<T, U>(arg: T): U { ... } "],
                "answer": 1,
                "explanation": "Generics use angle brackets (<T>) to define type parameters."
            },
            {
                "question": " What does the ! operator do in const value = document.getElementById('id')!?",
                "options": ["Throws an error if null "  ,"Asserts non-null value","Converts null to undefined ","Marks the variable as optional  "],
                "answer": 1,
                "explanation": "The non-null assertion operator (!) tells TypeScript the value won’t be null/undefined."
            },
            {
                "question": "  What does keyof do?",
                "options": [" Checks if a key exists "  ,"Maps object keys to values"," Returns union of an object’s keys ","Iterates over object keys  "],
                "answer": 2,
                "explanation": "Returns union of an object’s keys."
            },
            ]
    },
    5: {
        "technology": "TAILWIND CSS",
        "questions": [
            {
                "question": "What is Tailwind CSS?",
                "options": ["A JavaScript framework", "A component-based CSS framework", "A utility-first CSS framework", "A preprocessor like SASS"],
                "answer": 2,
                "explanation": "it provides utility classes for styling elements directly in HTML without writing custom CSS. It is not component-based like Bootstrap, nor is it a CSS preprocessor."
            },
             {
                "question": " Which of the following is NOT a valid Tailwind CSS utility class?",
                "options": ["text-center "  ,"bg-blue-500","margin-10 ","flex  "],
                "answer": 2,
                "explanation": " Tailwind uses m-10 instead of margin-10 for margin spacing. The correct syntax follows the pattern of m (margin) or p (padding) followed by a size value."
            },
             {
                "question": "What does the class flex do in Tailwind CSS?",
                "options": ["Aligns items to the center "  ,"Sets flex-direction to column","Enables CSS grid layout ","Sets the display property to flex  "],
                "answer": 3,
                "explanation": "The flex class applies display: flex to an element, allowing its child elements to be aligned using flexbox properties."
            },
             {
                "question": " How can you customize Tailwind CSS styles?",
                "options": ["By modifying styles.css directly"  ,"Using the tailwind.config.js file","By using inline styles only ","Tailwind CSS is not customizable  "],
                "answer": 1,
                "explanation": "Tailwind allows customization via the tailwind.config.js file, where you can extend the default theme, add custom colors, fonts, and more."
            },
             {
                "question": "  Which of the following is the correct way to apply responsive design in Tailwind CSS?",
                "options": ["@media(md):flex"   ,"md:flex","responsive:flex ","flex  "],
                "answer": 1,
                "explanation": "Tailwind CSS uses breakpoint prefixes such as sm:, md:, lg:, xl:, and 2xl: to apply styles at specific screen widths. Example: md:flex makes the element display: flex on medium screens and larger."
            },
             {
                "question": " What does the class p-4 do in Tailwind CSS?",
                "options": ["Sets padding to 4rem "  ,"Sets padding to 4px"," Sets padding to 1rem (16px)"," Sets padding to 4% "],
                "answer": 2,
                "explanation": "Tailwind uses a spacing scale, where p-4 applies padding: 16px (1rem). The values are based on a 4px increment system (e.g., p-1 = 4px, p-2 = 8px, p-4 = 16px, etc.)."
            },
             {
                "question": " What is the purpose of the group utility in Tailwind CSS?",
                "options": ["It is used for grouping flexbox items "  ,"It groups elements for styling based on parent states ","t creates CSS grid groups ","It enables media queries  "],
                "answer": 1,
                "explanation": "The group utility in Tailwind allows child elements to react to the state of their parent."
            },
             {
                "question": "Which Tailwind class applies a shadow effect?",
                "options": ["shadow-md "  ,"text-shadow","box-shadow ","drop-shadow  "],
                "answer": 0,
                "explanation": "Tailwind provides built-in shadow utilities like shadow-sm, shadow-md, shadow-lg, shadow-xl, and shadow-2xl to apply different levels of shadow effects. text-shadow and box-shadow are not valid Tailwind classes."
            },
             {
                "question": "Which utility class is used to set an element’s width to 100% of its parent?",
                "options": ["width-100 "  ,"w-full","w-100 ","width-full  "],
                "answer": 1,
                "explanation": "In Tailwind CSS, w-full sets width: 100%. There is no class like width-100 or full-width."
            },
             {
                "question": " Which class would you use to apply a gradient background in Tailwind?",
                "options": ["bg-gradient "  ,"gradient-bg","bg-gradient-to-r from-blue-500 to-green-500  ","background-gradient  "],
                "answer": 2,
                "explanation": "Tailwind CSS provides gradient utilities using bg-gradient-to-{direction} from-{color} to-{color}."
            },
        ]

},
         6: {
        "technology": "NEXT JS",
        "questions": [
            {
                "question": "What is the primary purpose of getStaticPaths in Next.js?",
                "options": ["Fetch data at request time", " Define dynamic routes for SSG", "Handle API routes", "Configure middleware"],
                "answer": 1,
                "explanation": "getStaticPaths generates paths for static pages during build time (used with getStaticProps)."
            },
            {
                 "question": " Which rendering method updates static pages at runtime after deployment?",
                "options": ["SSR (Server-Side Rendering)", "SSG (Static Site Generation)", "ISR (Incremental Static Regeneration)","CSR (Client-Side Rendering)"],
                "answer": 2,
                "explanation": "ISR regenerates static pages periodically or on-demand after deployment."
            },
            {
                 "question": "How do you create a dynamic route for blog posts?",
                "options": ["pages/blog/[slug].js", "pages/blog/slug.js", "Both a and b","pages/blog/:slug.js"],
                "answer": 0,
                "explanation": "Next.js uses square brackets ([]) for dynamic route parameters."
            },
            {
                 "question": "What is the purpose of the next/image component?",
                "options": ["Lazy-load images", "Optimize image file size", "Serve responsive images","All of the above"],
                "answer": 3,
                "explanation": " next/image automates image optimization, lazy loading, and responsive sizing."
            },
            {
                 "question": "What is the default port for the Next.js development server?",
                "options": ["8080", "3000", "5000","4060"],
                "answer": 1,
                "explanation": "Runs on localhost:3000 by default (npm run dev)."
            },
            {
                 "question": "How do you create an API endpoint in Next.js?",
                "options": ["api/users.js","pages/api/user.js",  "server/api/users.js","src/api/users.js"],
                "answer": 1,
                "explanation": "Next.js API routes are stored in the pages/api directory."
            },
            {
                 "question": "Which file configures Next.js settings like environment variables?",
                "options": ["next-env.d.ts", " package.json", "next.config.js","vercel.json"],
                "answer": 2,
                "explanation": "Custom configurations (e.g., redirects, headers) are added here."
            },
            {
                 "question": "Which method fetches data at build time for static pages?",
                "options": ["getServerSideProps", " getStaticProps", "useEffect","getInitialProps"],
                "answer": 1,
                "explanation": "getStaticProps pre-renders pages at build time (SSG)."
            },
            {
                 "question": " How do you handle 404 errors in Next.js?",
                "options": [ "Use next/error", "Add middleware","Configure _error.js" ,"Create pages/404.js"],
                "answer": 3,
                "explanation": "A custom 404.js file auto-handles 404 pages"
            },
            {
                 "question": "What does next/link do?",
                "options": ["Prefetch linked pages", " Enable client-side navigation", "Improve SEO","All of the above"],
                "answer": 3,
                "explanation": "The <Link> component optimizes routing with prefetching and client-side transitions."
            },
        ]
           },
         7: {
        "technology": "PYTHON",
        "questions": [
            {
                "question": "What is the output of print(type(3.14))?",
                "options": ["<class 'int'>", " <class 'float'>", "<class 'double'>", " <class 'decimal'>"],
                "answer": 1,
                "explanation": "Python uses float for decimal numbers."
            },
            {
                "question": "Which is used to create a comment in Python?",
                "options": ["//", " /* */", "#", "<!-- -->"],
                "answer": 2,
                "explanation": "# is used for single-line comments."
            },
            {
                "question": "What does 'hello'[1:4] return?",
                "options": ["'hel'", "'ell'", "'ello'", "'lo'"],
                "answer": 1,
                "explanation": "Slicing is inclusive of the start index and exclusive of the end index."
            },
            {
                "question": "Which is NOT a valid data structure?",
                "options": ["list", "data", "tuple", "array"],
                "answer": 3,
                "explanation": "Python has list, tuple, dict, and set—not a base array type (use list or array module)."
            },
            {
                "question": " What is the output of print(2 ** 3)?",
                "options": ["6", "8", "9", "23"],
                "answer": 1,
                "explanation": "** is the exponent operator (2^3 = 8)."
            },
            {
                "question": "Which loop is used to iterate over a sequence?",
                "options": ["while", "do-while", "for", "repeat"],
                "answer": 2,
                "explanation": "for loops iterate over sequences (lists, tuples, strings, etc.)."
            },
            {
                "question": "What is the result of bool("")?",
                "options": ["True", "False", "Error", "None"],
                "answer": 1,
                "explanation": "Empty strings are falsy in Python."
            },
            {
                "question": "How to read input from the user?",
                "options": ["readline()", "scan()", "input()", "get()"],
                "answer": 2,
                "explanation": "input() reads user input as a string."
            },
            {
                "question": "Which method adds an item to a list?",
                "options": ["insert()", "push()", "add()", "append()"],
                "answer": 3,
                "explanation": "append() adds an item to the end of a list."
            },
            {
                "question": "What does range(3) generate?",
                "options": ["[ 1, 2, 3]", "[0, 1, 2]", "[3]", "[0, 3]"],
                "answer": 1,
                "explanation": "range(n) generates values from 0 to n-1."
            },
        ]
         },
}
          
def show_question(question_data, q_num):
    with st.container():
        st.markdown(f'<div class="question-box">', unsafe_allow_html=True)
        st.markdown(f"**Q{q_num+1}:** {question_data['question']}")
        
        answer = st.radio(
            "Select answer:",
            question_data['options'],
            key=f"day{st.session_state.current_day}_q{q_num}",
            disabled=st.session_state.current_day in st.session_state.answers
        )
        
        if st.session_state.show_explanations:
            correct_answer = question_data['options'][question_data['answer']]
            if answer == correct_answer:
                st.markdown(f"<div style='color: green; margin-top: 1rem;'>✅ Correct! {question_data['explanation']}</div>", 
                           unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color: red; margin-top: 1rem;'>❌ Correct answer: {correct_answer}<br>{question_data['explanation']}</div>", 
                           unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def get_ai_response(user_input):
    """Generate meaningful responses based on user questions"""
    user_input = user_input.lower()
    
    tech_keywords = {
        'html': QUESTIONS[1],
        'css': QUESTIONS[2],
        'javascript': QUESTIONS[3],
        'typescript': QUESTIONS[4],
        'tailwind': QUESTIONS[5],
        'next.js': QUESTIONS[6],
        'python': QUESTIONS[7]
    }
    
    for tech, data in tech_keywords.items():
        if tech in user_input:
            return f"**{data['technology']}**: {data['questions'][0]['explanation']}"
    
    return "I'm here to help with web development concepts! Ask me about:\n- HTML\n- CSS\n- JavaScript\n- TypeScript\n- Tailwind\n- Next.js\n- Python"

def chat_key(key_suffix):
    return f"chat_{hash('chat_interface')}_{key_suffix}"

def chat_interface():
    """AI Chat Assistant Component"""
    def chat_key(key_suffix):
        return f"chat_{hash('chat_interface')}_{key_suffix}"

    # Initialize chat state
    if 'chat_visible' not in st.session_state:
        st.session_state.chat_visible = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Chat toggle button
    st.markdown("""
    <style>
        .chat-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 9999;
        }
        .chat-container {
            position: fixed;
            bottom: 100px;
            right: 30px;
            z-index: 9998;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            width: 350px;
            max-height: 60vh;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)
    
    if st.button("🤖", key=chat_key("toggle_button")):
        st.session_state.chat_visible = not st.session_state.chat_visible
        st.rerun()

    # Chat container
    if st.session_state.chat_visible:
        with st.container():
            st.markdown("""
            <div class="chat-container">
                <div class="chat-header" style="
                    background: #1F63DA;
                    color: white;
                    padding: 1rem;
                    border-radius: 15px 15px 0 0;
                    font-weight: bold;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                ">
                    <span>📚 Ask Questions About MCQ Topics</span>
                    <span style="cursor: pointer;" onclick="document.dispatchEvent(new CustomEvent('closeChat'))">×</span>
                </div>
                <div class="chat-messages" style="
                    padding: 1rem;
                    height: 400px;
                    overflow-y: auto;
                ">
            """, unsafe_allow_html=True)
            
            # Display messages
            for msg in st.session_state.chat_history:
                if msg['type'] == 'user':
                    st.markdown(f'<div class="message user-message">👤 {msg["content"]}</div>', 
                               unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="message bot-message">🤖 {msg["content"]}</div>', 
                               unsafe_allow_html=True)
            
            st.markdown('</div></div>', unsafe_allow_html=True)
            
            # Chat input and controls
            with st.form(key=chat_key("chat_form")):
                user_input = st.text_input("Type your message:", key=chat_key("input_field"))
                if st.form_submit_button("Send"):
                    if user_input:
                        # Add user message
                        st.session_state.chat_history.append({
                            'type': 'user',
                            'content': user_input
                        })
                        
                        # Generate and add bot response
                        bot_response = get_ai_response(user_input)  # Now properly defined
                        st.session_state.chat_history.append({
                            'type': 'bot',
                            'content': bot_response
                        })
                        st.rerun()

# Add JavaScript to handle close button
st.markdown("""
<script>
document.addEventListener('closeChat', function() {
    window.parent.document.querySelector('[data-testid="stButton"]').click();
});
</script>
""", unsafe_allow_html=True)
def show_completion_screen():
    """Final completion screen with working restart button"""
    st.markdown("""
    <style>
        .restart-btn {
            background: #1F63DA !important;
            color: white !important;
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-size: 1.1rem;
            cursor: pointer;
            width: 100%;
            margin: 2rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Restart button with session state reset
    if st.button("Restart Challenge", key="restart_btn"):
        st.session_state.update({
            'current_day': 1,
            'score': 0,
            'answers': {},
            'show_explanations': False,
            'chat_visible': False,
            'chat_history': []
        })
        st.rerun()

    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.9);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem auto;
        max-width: 600px;
    ">
        <h1 style="color: #1F63DA; font-size: 2.5rem;">🎉 Challenge Complete! 🎉</h1>
        <p style="font-size: 1.5rem;">Total Score: {}/70</p>
    </div>
    """.format(st.session_state.score), unsafe_allow_html=True)

def main():
    st.markdown('<p class="header-text">🚀 7-Days Web Dev Challenge</p>', unsafe_allow_html=True)
    
    # Chat interface
    chat_interface()
    
    # Completion screen
    if st.session_state.current_day > 7:
        show_completion_screen()
        st.stop()
    
    # Progress tracking
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="score-card">Current Day: {st.session_state.current_day}/7</div>', 
                    unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="score-card">Total Score: {st.session_state.score}/70</div>', 
                    unsafe_allow_html=True)
    
    # Daily questions
    try:
        day_data = QUESTIONS[st.session_state.current_day]
    except KeyError:
        st.error("Invalid day selection!")
        st.stop()
    
    st.header(f"Day {st.session_state.current_day}: {day_data['technology']}")
    
    # Display questions
    for q_num, question in enumerate(day_data["questions"]):
        show_question(question, q_num)
    
    # Answer submission
    if st.session_state.current_day not in st.session_state.answers:
        if st.button("Submit Answers"):
            day_score = 0
            for q_num, question in enumerate(day_data["questions"]):
                user_answer = st.session_state.get(f"day{st.session_state.current_day}_q{q_num}")
                if user_answer == question["options"][question["answer"]]:
                    day_score += 1
            st.session_state.score += day_score
            st.session_state.answers[st.session_state.current_day] = day_score
            st.session_state.show_explanations = True
            st.rerun()
    else:
        st.success(f"✔️ Day {st.session_state.current_day} completed! Score: {st.session_state.answers[st.session_state.current_day]}/10")
        if st.button("Toggle Explanations"):
            st.session_state.show_explanations = not st.session_state.show_explanations
            st.rerun()
    
    # Navigation
    col1, col2 = st.columns(2)
    if st.session_state.current_day > 1:
        with col1:
            if st.button("⬅️ Previous Day"):
                st.session_state.current_day -= 1
                st.session_state.show_explanations = False
                st.rerun()
    if st.session_state.current_day <= 7:
        with col2:
            if st.session_state.current_day in st.session_state.answers:
                if st.button("Next Day ➡️" if st.session_state.current_day < 7 else "Final Submit 🏁"):
                    st.session_state.current_day += 1
                    st.session_state.show_explanations = False
                    st.rerun()

if __name__ == "__main__":
    main()