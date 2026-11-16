"""Extra answer-bank entries added in the Nov 16, 2026 rebuild.

Same shape as ANSWERS in answers.py, plus "category" and "difficulty"
used by the topic browser. Every answer follows the AI-era style:
pattern -> why it works -> complexity -> trade-off / interview tip.

New topics have full Hinglish + English answers and concise code-mixed
answers in Telugu, Tamil, Kannada and Malayalam (tech terms stay in
English, as students actually speak them). If a language version is
ever missing, answers.py falls back to the English text.
"""

EXTRA_ANSWERS = [
    {
        "topic": "Binary Search",
        "category": "Arrays & Searching",
        "difficulty": "Easy",
        "keywords": ["binary search", "binarysearch", "bainari search", "sorted array search", "log n search", "द्विआधारी खोज", "బైనరీ సెర్చ్", "பைனரி சர்ச்", "ಬೈನರಿ ಸರ್ಚ್", "ബൈനറി സെർച്ച്"],
        "answers": {
            "hinglish": (
                "Pattern hai divide and conquer, sorted array par. Mid element ko target se compare karo. "
                "Target chhota hai toh left half mein jao, bada hai toh right half mein. Har step mein search "
                "space aadha ho jata hai, isliye ye linear scan se bahut tez hai. Time hai O of log n, space O of 1. "
                "Trade-off: array sorted hona zaroori hai. Sorted nahi hai toh pehle sort karna padega, jo O of n log n hai. "
                "Interview mein overflow-safe mid, matlab low plus high minus low by two, bolna achha lagta hai."
            ),
            "english": (
                "The pattern is divide and conquer on a sorted array. Compare the middle element with the target. "
                "If the target is smaller, search the left half; if larger, the right half. Each step halves the "
                "search space, so it is far faster than a linear scan. Time is O of log n, space O of 1. "
                "The trade-off: the array must be sorted. If it is not, sorting first costs O of n log n. "
                "In an interview, mention the overflow-safe midpoint: low plus half of high minus low."
            ),
            "telugu": (
                "Pattern: sorted array పై divide and conquer. Middle element ని target తో compare చేయండి. "
                "Target చిన్నదైతే left half, పెద్దదైతే right half వెతకండి. ప్రతి step లో search space సగం అవుతుంది. "
                "Time O(log n), space O(1). Array sorted గా ఉండాలి — లేకపోతే ముందు sort చేయాలి, అది O(n log n)."
            ),
            "tamil": (
                "Pattern: sorted array மீது divide and conquer. Middle element-ஐ target உடன் compare செய்யுங்கள். "
                "Target சிறியதாக இருந்தால் left half, பெரியதாக இருந்தால் right half தேடுங்கள். ஒவ்வொரு step-லும் "
                "search space பாதியாகிறது. Time O(log n), space O(1). Array sorted ஆக இருக்க வேண்டும் — இல்லையெனில் முதலில் sort செய்ய வேண்டும்."
            ),
            "kannada": (
                "Pattern: sorted array ಮೇಲೆ divide and conquer. Middle element ಅನ್ನು target ಜೊತೆ compare ಮಾಡಿ. "
                "Target ಚಿಕ್ಕದಾಗಿದ್ದರೆ left half, ದೊಡ್ಡದಾಗಿದ್ದರೆ right half ಹುಡುಕಿ. ಪ್ರತಿ step ನಲ್ಲಿ search space ಅರ್ಧವಾಗುತ್ತದೆ. "
                "Time O(log n), space O(1). Array sorted ಆಗಿರಬೇಕು — ಇಲ್ಲದಿದ್ದರೆ ಮೊದಲು sort ಮಾಡಬೇಕು, ಅದು O(n log n)."
            ),
            "malayalam": (
                "Pattern: sorted array-യിൽ divide and conquer. Middle element-നെ target-മായി compare ചെയ്യുക. "
                "Target ചെറുതാണെങ്കിൽ left half, വലുതാണെങ്കിൽ right half തിരയുക. ഓരോ step-ലും search space പകുതിയാകും. "
                "Time O(log n), space O(1). Array sorted ആയിരിക്കണം — അല്ലെങ്കിൽ ആദ്യം sort ചെയ്യണം, അത് O(n log n) ആണ്."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: beech wala element dekho, target usse chhota hai ya bada, us hisaab se aadha array hata do. Baar baar yehi karo.",
            "english": "Simply: look at the middle element, discard the half that cannot contain the target, and repeat.",
        },
        "example": "Example: nums = [1, 3, 5, 7, 9], target = 7. Mid = 5, target bigger, go right. Mid = 7, found at index 3.",
    },
    {
        "topic": "Merge Intervals",
        "category": "Arrays & Searching",
        "difficulty": "Medium",
        "keywords": ["merge intervals", "merge interval", "overlapping intervals", "interval merge", "merge overlapping"],
        "answers": {
            "hinglish": (
                "Pattern hai sort karke merge. Intervals ko start time ke hisaab se sort karo, phir ek ek karke dekho. "
                "Agar current interval pichhle merged interval se overlap karta hai, toh end ko max tak badhao. Nahi toh naya interval shuru karo. "
                "Sorting ki wajah se overlap check sirf pichhle interval se karna padta hai. Time hai O of n log n sorting ke liye, space O of n output ke liye. "
                "Trade-off: input ko sort karna padta hai, original order kho jata hai. Yehi pattern meeting rooms aur insert interval mein bhi kaam aata hai."
            ),
            "english": (
                "The pattern is sort, then merge. Sort the intervals by start time, then walk through them once. "
                "If the current interval overlaps the last merged one, extend its end to the maximum. Otherwise, start a new interval. "
                "Sorting means you only ever compare with the previous merged interval. Time is O of n log n for sorting, space O of n for the output. "
                "The trade-off: you lose the original order. The same pattern solves meeting rooms and insert interval."
            ),
            "telugu": (
                "Pattern: start time ప్రకారం sort చేసి merge చేయండి. Current interval గత interval తో overlap అయితే end ని max వరకు పెంచండి, "
                "లేకపోతే కొత్త interval మొదలుపెట్టండి. Time O(n log n), space O(n). Sorting వల్ల original order పోతుంది — ఇదే trade-off."
            ),
            "tamil": (
                "Pattern: start time படி sort செய்து merge செய்யுங்கள். Current interval முந்தைய interval உடன் overlap ஆனால் end-ஐ max வரை நீட்டவும், "
                "இல்லையெனில் புதிய interval தொடங்கவும். Time O(n log n), space O(n). Sorting-ஆல் original order போய்விடும் — அதுதான் trade-off."
            ),
            "kannada": (
                "Pattern: start time ಪ್ರಕಾರ sort ಮಾಡಿ merge ಮಾಡಿ. Current interval ಹಿಂದಿನ interval ಜೊತೆ overlap ಆದರೆ end ಅನ್ನು max ವರೆಗೆ ವಿಸ್ತರಿಸಿ, "
                "ಇಲ್ಲದಿದ್ದರೆ ಹೊಸ interval ಶುರು ಮಾಡಿ. Time O(n log n), space O(n). Sorting ನಿಂದ original order ಕಳೆದುಹೋಗುತ್ತದೆ — ಅದೇ trade-off."
            ),
            "malayalam": (
                "Pattern: start time അനുസരിച്ച് sort ചെയ്ത് merge ചെയ്യുക. Current interval മുൻ interval-മായി overlap ആയാൽ end max വരെ നീട്ടുക, "
                "ഇല്ലെങ്കിൽ പുതിയ interval തുടങ്ങുക. Time O(n log n), space O(n). Sorting കാരണം original order നഷ്ടമാകും — അതാണ് trade-off."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: pehle sort karo, phir chipke hue intervals ko ek bada interval bana do.",
            "english": "Simply: sort first, then glue together any intervals that touch or overlap.",
        },
        "example": "Example: [[1,3],[2,6],[8,10],[15,18]] -> [[1,6],[8,10],[15,18]].",
    },
    {
        "topic": "Trapping Rain Water",
        "category": "Arrays & Searching",
        "difficulty": "Hard",
        "keywords": ["trapping rain water", "trap rain water", "rain water", "rainwater", "trapped water", "water trapped"],
        "answers": {
            "hinglish": (
                "Pattern hai two pointers with left max aur right max. Har position par rukne wala paani min of left max and right max minus height hota hai. "
                "Do pointer, left aur right, chhoti side se aage badhte hain, kyunki paani chhoti deewar se decide hota hai. "
                "Time hai O of n, space O of 1. Trade-off: do extra arrays se left max aur right max pehle nikaalna samajhna aasan hai, lekin O of n space leta hai. "
                "Two pointer version wahi kaam bina extra space ke karta hai, bas logic thoda dhyaan se bolna padta hai."
            ),
            "english": (
                "The pattern is two pointers tracking the left maximum and right maximum. The water held at any position is the minimum of the two maxima minus its height. "
                "The pointers advance from the smaller side, because water is limited by the shorter wall. "
                "Time is O of n, space O of 1. The trade-off: precomputing left and right maxima in two arrays is easier to explain but costs O of n space. "
                "The two-pointer version does the same work with no extra space, at the cost of trickier reasoning."
            ),
            "telugu": (
                "Pattern: left max, right max తో two pointers. ప్రతి position లో నీరు = min(left max, right max) minus height. "
                "చిన్న side నుంచి pointers ముందుకు వెళ్తాయి. Time O(n), space O(1). రెండు arrays వాడితే అర్థం చేసుకోవడం సులభం, కానీ O(n) space పడుతుంది."
            ),
            "tamil": (
                "Pattern: left max, right max உடன் two pointers. ஒவ்வொரு position-லும் நீர் = min(left max, right max) minus height. "
                "சிறிய பக்கத்திலிருந்து pointers முன்னேறும். Time O(n), space O(1). இரண்டு arrays பயன்படுத்தினால் புரிவது எளிது, ஆனால் O(n) space ஆகும்."
            ),
            "kannada": (
                "Pattern: left max, right max ಜೊತೆ two pointers. ಪ್ರತಿ position ನಲ್ಲಿ ನೀರು = min(left max, right max) minus height. "
                "ಚಿಕ್ಕ ಬದಿಯಿಂದ pointers ಮುಂದುವರಿಯುತ್ತವೆ. Time O(n), space O(1). ಎರಡು arrays ಬಳಸಿದರೆ ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು ಸುಲಭ, ಆದರೆ O(n) space ಬೇಕು."
            ),
            "malayalam": (
                "Pattern: left max, right max എന്നിവയോടെ two pointers. ഓരോ position-ലും വെള്ളം = min(left max, right max) minus height. "
                "ചെറിയ വശത്ത് നിന്ന് pointers മുന്നോട്ട് പോകും. Time O(n), space O(1). രണ്ട് arrays ഉപയോഗിച്ചാൽ മനസ്സിലാക്കാൻ എളുപ്പം, പക്ഷേ O(n) space വേണം."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: har jagah paani utna rukta hai jitni chhoti deewar allow karti hai, apni height minus karke.",
            "english": "Simply: at each spot, water is limited by the shorter of the tallest walls on either side, minus your own height.",
        },
        "example": "Example: height = [0,1,0,2,1,0,1,3,2,1,2,1] -> trapped water = 6.",
    },
    {
        "topic": "Maximum Subarray (Kadane's Algorithm)",
        "category": "Arrays & Searching",
        "difficulty": "Medium",
        "keywords": ["maximum subarray", "max subarray", "kadane", "kadane's", "largest sum subarray", "maximum sum subarray"],
        "answers": {
            "hinglish": (
                "Pattern hai Kadane's algorithm, greedy running sum. Chalte hue sum ko track karo, aur jab sum negative ho jaye toh use zero se restart karo, "
                "kyunki negative prefix aage ke sum ko sirf kam karega. Har step par best sum update karte raho. "
                "Time hai O of n, space O of 1. Trade-off: ye sirf maximum sum deta hai, subarray ka start aur end bhi chahiye toh extra tracking karni padegi. "
                "Edge case: saare numbers negative hon toh answer sabse bada, matlab sabse kam negative, number hota hai."
            ),
            "english": (
                "The pattern is Kadane's algorithm: a greedy running sum. Track the current sum, and restart it at zero whenever it goes negative, "
                "because a negative prefix can only drag the future sum down. Keep the best sum seen so far. "
                "Time is O of n, space O of 1. The trade-off: this gives only the maximum sum; to also return the subarray bounds you need extra tracking. "
                "Edge case: if every number is negative, the answer is the largest, least negative, number."
            ),
            "telugu": (
                "Pattern: Kadane's algorithm. Running sum track చేయండి; sum negative అయితే zero నుంచి restart చేయండి, "
                "ఎందుకంటే negative prefix ముందు sum ని తగ్గిస్తుంది. Time O(n), space O(1). అన్ని numbers negative అయితే, అతిపెద్ద number ఏ answer."
            ),
            "tamil": (
                "Pattern: Kadane's algorithm. Running sum-ஐ track செய்யுங்கள்; sum negative ஆனால் zero-விலிருந்து restart செய்யுங்கள், "
                "ஏனெனில் negative prefix எதிர்கால sum-ஐ குறைக்கும். Time O(n), space O(1). எல்லா numbers-ம் negative என்றால், மிகப்பெரிய number தான் answer."
            ),
            "kannada": (
                "Pattern: Kadane's algorithm. Running sum track ಮಾಡಿ; sum negative ಆದರೆ zero ನಿಂದ restart ಮಾಡಿ, "
                "ಏಕೆಂದರೆ negative prefix ಮುಂದಿನ sum ಅನ್ನು ಕಡಿಮೆ ಮಾಡುತ್ತದೆ. Time O(n), space O(1). ಎಲ್ಲಾ numbers negative ಆದರೆ, ದೊಡ್ಡ number ಏ answer."
            ),
            "malayalam": (
                "Pattern: Kadane's algorithm. Running sum track ചെയ്യുക; sum negative ആയാൽ zero-യിൽ നിന്ന് restart ചെയ്യുക, "
                "കാരണം negative prefix ഭാവി sum കുറയ്ക്കും. Time O(n), space O(1). എല്ലാ numbers-ഉം negative ആണെങ്കിൽ, ഏറ്റവും വലിയ number ആണ് answer."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: sum jodte jao, jab sum negative ho toh naya shuru karo, best sum yaad rakho.",
            "english": "Simply: keep adding, restart when the running sum turns negative, and remember the best sum you saw.",
        },
        "example": "Example: nums = [-2,1,-3,4,-1,2,1,-5,4] -> maximum sum = 6, from [4,-1,2,1].",
    },
    {
        "topic": "Group Anagrams",
        "category": "Strings & Hashing",
        "difficulty": "Medium",
        "keywords": ["group anagrams", "group anagram", "anagram groups", "grouping anagrams"],
        "answers": {
            "hinglish": (
                "Pattern hai hash map with a canonical key. Har word ke liye ek key banao jo uske saare anagrams ke liye same ho. "
                "Do tareeke hain: letters ko sort karke key banana, ya 26 letters ki count ko key banana. Count wala tareeka tez hai. "
                "Phir same key wale words ek hi group mein daal do. Time hai O of n into k, jahan k word ki length hai, count key ke saath. "
                "Trade-off: sort key likhna aasan hai lekin O of k log k leta hai. Count key tez hai par key banana thoda lamba hai."
            ),
            "english": (
                "The pattern is a hash map with a canonical key. For each word, build a key that is identical for all of its anagrams. "
                "Two ways: sort the letters to form the key, or count the 26 letters to form the key. Counting is faster. "
                "Then place words with the same key in one group. Time is O of n times k, where k is word length, with the counting key. "
                "The trade-off: the sort key is easier to write but costs O of k log k. The count key is faster but more code."
            ),
            "telugu": (
                "Pattern: canonical key తో hash map. ప్రతి word కి, దాని anagrams అన్నిటికీ ఒకేలా ఉండే key తయారుచేయండి — "
                "letters sort చేయడం లేదా 26 letters count చేయడం. Count key వేగంగా ఉంటుంది. Time O(n x k). Sort key సులభం, కానీ O(k log k)."
            ),
            "tamil": (
                "Pattern: canonical key உடன் hash map. ஒவ்வொரு word-க்கும், அதன் anagrams அனைத்திற்கும் ஒரே மாதிரியான key உருவாக்குங்கள் — "
                "letters-ஐ sort செய்வது அல்லது 26 letters-ஐ count செய்வது. Count key வேகமானது. Time O(n x k). Sort key எளிது, ஆனால் O(k log k)."
            ),
            "kannada": (
                "Pattern: canonical key ಜೊತೆ hash map. ಪ್ರತಿ word ಗೆ, ಅದರ ಎಲ್ಲಾ anagrams ಗೆ ಒಂದೇ ರೀತಿಯ key ಮಾಡಿ — "
                "letters sort ಮಾಡುವುದು ಅಥವಾ 26 letters count ಮಾಡುವುದು. Count key ವೇಗವಾಗಿದೆ. Time O(n x k). Sort key ಸುಲಭ, ಆದರೆ O(k log k)."
            ),
            "malayalam": (
                "Pattern: canonical key-യോടെ hash map. ഓരോ word-നും, അതിന്റെ എല്ലാ anagrams-നും ഒരേപോലെയുള്ള key ഉണ്ടാക്കുക — "
                "letters sort ചെയ്യുകയോ 26 letters count ചെയ്യുകയോ. Count key വേഗമാണ്. Time O(n x k). Sort key എളുപ്പം, പക്ഷേ O(k log k)."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: jo words ek jaise letters se bane hain, unhe ek hi dabbe mein daal do. Dabbe ka naam letters ki count hai.",
            "english": "Simply: put words built from the same letters in the same box, and label the box by its letter counts.",
        },
        "example": "Example: [eat, tea, tan, ate, nat, bat] -> [[eat,tea,ate],[tan,nat],[bat]].",
    },
    {
        "topic": "Longest Palindromic Substring",
        "category": "Strings & Hashing",
        "difficulty": "Medium",
        "keywords": ["longest palindromic substring", "palindromic substring", "longest palindrome", "palindrome substring", "expand around center", "expand around centre"],
        "answers": {
            "hinglish": (
                "Pattern hai expand around centre. Har position ko centre maan ke dono taraf failo, jab tak characters match karte rahen. "
                "Do tarah ke centre hote hain: ek character wala odd length, aur do character wala even length. Dono check karna zaroori hai. "
                "Time hai O of n square, space O of 1. Trade-off: Manacher's algorithm O of n mein karta hai, lekin interview mein likhna aur samjhana mushkil hai. "
                "Expand around centre samajhna aasan hai aur aksar acceptable hota hai, bas dono centre types mat bhoolna."
            ),
            "english": (
                "The pattern is expand around centre. Treat every position as a centre and grow outwards while the characters match. "
                "There are two centre types: a single character for odd lengths, and two characters for even lengths. You must check both. "
                "Time is O of n squared, space O of 1. The trade-off: Manacher's algorithm runs in O of n, but it is hard to write and explain in an interview. "
                "Expand around centre is easy to reason about and usually acceptable, as long as you handle both centre types."
            ),
            "telugu": (
                "Pattern: centre చుట్టూ expand చేయడం. ప్రతి position ని centre గా తీసుకుని, characters match అయ్యేవరకు రెండు వైపులా విస్తరించండి. "
                "Odd length కి ఒక character, even length కి రెండు characters — రెండూ check చేయాలి. Time O(n square), space O(1). Manacher's O(n), కానీ కష్టం."
            ),
            "tamil": (
                "Pattern: centre-ஐ சுற்றி expand செய்வது. ஒவ்வொரு position-ஐயும் centre ஆக எடுத்து, characters match ஆகும் வரை இரு பக்கமும் விரிவாக்குங்கள். "
                "Odd length-க்கு ஒரு character, even length-க்கு இரண்டு characters — இரண்டையும் check செய்ய வேண்டும். Time O(n square), space O(1). Manacher's O(n), ஆனால் கடினம்."
            ),
            "kannada": (
                "Pattern: centre ಸುತ್ತ expand ಮಾಡುವುದು. ಪ್ರತಿ position ಅನ್ನು centre ಆಗಿ ತೆಗೆದುಕೊಂಡು, characters match ಆಗುವವರೆಗೆ ಎರಡೂ ಬದಿಗೆ ವಿಸ್ತರಿಸಿ. "
                "Odd length ಗೆ ಒಂದು character, even length ಗೆ ಎರಡು characters — ಎರಡನ್ನೂ check ಮಾಡಬೇಕು. Time O(n square), space O(1). Manacher's O(n), ಆದರೆ ಕಷ್ಟ."
            ),
            "malayalam": (
                "Pattern: centre-ന് ചുറ്റും expand ചെയ്യുക. ഓരോ position-നെയും centre ആയി എടുത്ത്, characters match ആകുന്നതുവരെ രണ്ട് വശത്തേക്കും വികസിപ്പിക്കുക. "
                "Odd length-ന് ഒരു character, even length-ന് രണ്ട് characters — രണ്ടും check ചെയ്യണം. Time O(n square), space O(1). Manacher's O(n), പക്ഷേ ബുദ്ധിമുട്ടാണ്."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: har jagah se beech se bahar ki taraf failo, jab tak dono taraf same letter mile. Sabse lamba wala jawab hai.",
            "english": "Simply: grow outwards from every possible centre while both sides match, and keep the longest one you find.",
        },
        "example": "Example: s = babad -> bab or aba. s = cbbd -> bb.",
    },
    {
        "topic": "Reverse Linked List",
        "category": "Linked List",
        "difficulty": "Easy",
        "keywords": ["reverse linked list", "reverse link list", "reverse a linked list", "reversing linked list", "linked list reverse", "reverse list", "रिवर्स लिंक्ड लिस्ट", "లింక్డ్ లిస్ట్ రివర్స్", "லிங்க்ட் லிஸ்ட் ரிவர்ஸ்", "ಲಿಂಕ್ಡ್ ಲಿಸ್ಟ್ ರಿವರ್ಸ್", "ലിങ്ക്ഡ് ലിസ്റ്റ് റിവേഴ്സ്"],
        "answers": {
            "hinglish": (
                "Pattern hai three pointers: previous, current, next. Har node par pehle next ko save karo, phir current ka next previous ki taraf mod do, "
                "phir previous aur current ko ek step aage badhao. Aakhir mein previous hi nayi head ban jata hai. "
                "Ye kaam karta hai kyunki hum ek ek karke har link ko ulta karte hain, list ko dobara banaye bina. "
                "Time hai O of n, space O of 1 iterative version mein. Recursive version bhi O of n time leta hai lekin call stack ke liye O of n space leta hai."
            ),
            "english": (
                "The pattern is three pointers: previous, current, and next. At each node, save next, flip current's next pointer to point at previous, "
                "then move previous and current one step forward. At the end, previous is the new head. "
                "It works because you reverse one link at a time without rebuilding the list. "
                "Time is O of n, space O of 1 for the iterative version. The recursive version also takes O of n time but O of n stack space."
            ),
            "telugu": (
                "Pattern: previous, current, next అనే మూడు pointers. ప్రతి node దగ్గర next ని save చేసి, current యొక్క next ని previous వైపు తిప్పండి, "
                "తర్వాత రెండింటినీ ముందుకు జరపండి. చివర్లో previous ఏ కొత్త head. Time O(n), space O(1). Recursive version కి O(n) stack space పడుతుంది."
            ),
            "tamil": (
                "Pattern: previous, current, next என்ற மூன்று pointers. ஒவ்வொரு node-லும் next-ஐ save செய்து, current-ன் next-ஐ previous பக்கம் திருப்புங்கள், "
                "பிறகு இரண்டையும் முன்னே நகர்த்துங்கள். முடிவில் previous தான் புதிய head. Time O(n), space O(1). Recursive version-க்கு O(n) stack space ஆகும்."
            ),
            "kannada": (
                "Pattern: previous, current, next ಎಂಬ ಮೂರು pointers. ಪ್ರತಿ node ನಲ್ಲಿ next ಅನ್ನು save ಮಾಡಿ, current ನ next ಅನ್ನು previous ಕಡೆಗೆ ತಿರುಗಿಸಿ, "
                "ನಂತರ ಎರಡನ್ನೂ ಮುಂದಕ್ಕೆ ಸರಿಸಿ. ಕೊನೆಯಲ್ಲಿ previous ಏ ಹೊಸ head. Time O(n), space O(1). Recursive version ಗೆ O(n) stack space ಬೇಕು."
            ),
            "malayalam": (
                "Pattern: previous, current, next എന്ന മൂന്ന് pointers. ഓരോ node-ലും next save ചെയ്ത്, current-ന്റെ next previous-ലേക്ക് തിരിക്കുക, "
                "പിന്നീട് രണ്ടും മുന്നോട്ട് നീക്കുക. അവസാനം previous ആണ് പുതിയ head. Time O(n), space O(1). Recursive version-ന് O(n) stack space വേണം."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: har node ka teer ulta kar do, ek ek karke, aakhir wala node head ban jayega.",
            "english": "Simply: flip each node's arrow one by one; the last node becomes the new head.",
        },
        "example": "Example: 1 -> 2 -> 3 -> null becomes 3 -> 2 -> 1 -> null.",
    },
    {
        "topic": "Linked List Cycle",
        "category": "Linked List",
        "difficulty": "Easy",
        "keywords": ["linked list cycle", "cycle in linked list", "detect cycle", "floyd cycle", "tortoise hare", "cycle detection linked list", "loop in linked list"],
        "answers": {
            "hinglish": (
                "Pattern hai Floyd's cycle detection, tortoise and hare. Ek slow pointer ek step chalta hai, ek fast pointer do step. "
                "Agar list mein cycle hai toh fast pointer slow ko peeche se pakad lega, kyunki woh gol gol ghoom rahe hain. Cycle nahi hai toh fast null tak pahunch jayega. "
                "Time hai O of n, space O of 1. Trade-off: visited nodes ko hash set mein rakhna samajhna aasan hai, lekin O of n space leta hai. "
                "Two pointer wala tareeka bina extra memory ke wahi jawab deta hai. Cycle ka start dhoondhna ho toh dono ko head se dobara chalana padta hai."
            ),
            "english": (
                "The pattern is Floyd's cycle detection: tortoise and hare. A slow pointer moves one step, a fast pointer moves two. "
                "If there is a cycle, the fast pointer will eventually catch the slow one from behind, since both keep looping. If there is no cycle, the fast pointer reaches null. "
                "Time is O of n, space O of 1. The trade-off: storing visited nodes in a hash set is easier to follow but costs O of n space. "
                "The two-pointer method gives the same answer with no extra memory. To find where the cycle starts, restart one pointer at the head."
            ),
            "telugu": (
                "Pattern: Floyd's tortoise and hare. Slow pointer ఒక step, fast pointer రెండు steps వెళ్తాయి. Cycle ఉంటే fast, slow ని పట్టుకుంటుంది; "
                "లేకపోతే fast null కి చేరుతుంది. Time O(n), space O(1). Hash set వాడితే సులభం, కానీ O(n) space పడుతుంది."
            ),
            "tamil": (
                "Pattern: Floyd's tortoise and hare. Slow pointer ஒரு step, fast pointer இரண்டு steps செல்லும். Cycle இருந்தால் fast, slow-ஐ பிடிக்கும்; "
                "இல்லையெனில் fast null-ஐ அடையும். Time O(n), space O(1). Hash set பயன்படுத்தினால் எளிது, ஆனால் O(n) space ஆகும்."
            ),
            "kannada": (
                "Pattern: Floyd's tortoise and hare. Slow pointer ಒಂದು step, fast pointer ಎರಡು steps ಹೋಗುತ್ತದೆ. Cycle ಇದ್ದರೆ fast, slow ಅನ್ನು ಹಿಡಿಯುತ್ತದೆ; "
                "ಇಲ್ಲದಿದ್ದರೆ fast null ತಲುಪುತ್ತದೆ. Time O(n), space O(1). Hash set ಬಳಸಿದರೆ ಸುಲಭ, ಆದರೆ O(n) space ಬೇಕು."
            ),
            "malayalam": (
                "Pattern: Floyd's tortoise and hare. Slow pointer ഒരു step, fast pointer രണ്ട് steps പോകും. Cycle ഉണ്ടെങ്കിൽ fast, slow-നെ പിടിക്കും; "
                "ഇല്ലെങ്കിൽ fast null-ൽ എത്തും. Time O(n), space O(1). Hash set ഉപയോഗിച്ചാൽ എളുപ്പം, പക്ഷേ O(n) space വേണം."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: ek dheere, ek tez. Tez wala dheere wale ko pakad le toh cycle hai, nahi toh nahi hai.",
            "english": "Simply: one slow, one fast. If the fast one laps the slow one, there is a cycle.",
        },
        "example": "Example: 3 -> 2 -> 0 -> -4, with -4 pointing back to 2 -> cycle present, answer true.",
    },
    {
        "topic": "Merge Two Sorted Lists",
        "category": "Linked List",
        "difficulty": "Easy",
        "keywords": ["merge two sorted lists", "merge sorted lists", "merge two sorted linked lists", "merge two lists"],
        "answers": {
            "hinglish": (
                "Pattern hai dummy node with two pointers. Ek dummy head banao, phir dono lists ke head ko compare karo. "
                "Chhota node dummy ki tail se jodo, aur us list ka pointer aage badhao. Ek list khatm ho jaye toh doosri list ka bacha hua hissa seedha jod do. "
                "Dummy node se edge cases aasan ho jate hain, head ko alag se handle nahi karna padta. "
                "Time hai O of n plus m, space O of 1 iterative version mein. Recursive version bhi same time leta hai, lekin stack space leta hai."
            ),
            "english": (
                "The pattern is a dummy node with two pointers. Create a dummy head, then compare the heads of both lists. "
                "Attach the smaller node to the dummy tail and advance that list's pointer. When one list runs out, attach the rest of the other directly. "
                "The dummy node removes edge cases, so you never handle the head separately. "
                "Time is O of n plus m, space O of 1 for the iterative version. The recursive version takes the same time but uses stack space."
            ),
            "telugu": (
                "Pattern: dummy node తో two pointers. Dummy head తయారుచేసి, రెండు lists heads ని compare చేయండి. చిన్న node ని tail కి జోడించి, "
                "ఆ list pointer ముందుకు జరపండి. ఒక list అయిపోతే మరొకటి మిగిలిన భాగం నేరుగా జోడించండి. Time O(n + m), space O(1)."
            ),
            "tamil": (
                "Pattern: dummy node உடன் two pointers. Dummy head உருவாக்கி, இரண்டு lists-ன் heads-ஐ compare செய்யுங்கள். சிறிய node-ஐ tail-ல் இணைத்து, "
                "அந்த list pointer-ஐ முன்னே நகர்த்துங்கள். ஒரு list முடிந்தால் மற்றதின் மீதியை நேரடியாக இணைக்கவும். Time O(n + m), space O(1)."
            ),
            "kannada": (
                "Pattern: dummy node ಜೊತೆ two pointers. Dummy head ಮಾಡಿ, ಎರಡು lists ನ heads ಅನ್ನು compare ಮಾಡಿ. ಚಿಕ್ಕ node ಅನ್ನು tail ಗೆ ಜೋಡಿಸಿ, "
                "ಆ list pointer ಅನ್ನು ಮುಂದಕ್ಕೆ ಸರಿಸಿ. ಒಂದು list ಮುಗಿದರೆ ಇನ್ನೊಂದರ ಉಳಿದ ಭಾಗವನ್ನು ನೇರವಾಗಿ ಜೋಡಿಸಿ. Time O(n + m), space O(1)."
            ),
            "malayalam": (
                "Pattern: dummy node-യോടെ two pointers. Dummy head ഉണ്ടാക്കി, രണ്ട് lists-ന്റെ heads compare ചെയ്യുക. ചെറിയ node tail-ൽ ചേർത്ത്, "
                "ആ list pointer മുന്നോട്ട് നീക്കുക. ഒരു list തീർന്നാൽ മറ്റേതിന്റെ ബാക്കി നേരിട്ട് ചേർക്കുക. Time O(n + m), space O(1)."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: dono ke pehle node mein se chhota wala lo, jodte jao, ek khatm ho toh doosri poori jod do.",
            "english": "Simply: always take the smaller of the two front nodes, and when one list ends, attach the rest of the other.",
        },
        "example": "Example: [1,2,4] + [1,3,4] -> [1,1,2,3,4,4].",
    },
    {
        "topic": "Remove Nth Node From End of List",
        "category": "Linked List",
        "difficulty": "Medium",
        "keywords": ["remove nth node from end", "remove nth from end", "nth node from end", "remove node from end linked list"],
        "answers": {
            "hinglish": (
                "Pattern hai two pointers with a fixed gap. Pehle fast pointer ko n steps aage bhejo, phir slow aur fast ko saath chalao. "
                "Jab fast end tak pahunchega, slow us node par hoga jise hatana hai usse just pehle. Phir slow ka next skip kar do. "
                "Dummy node use karo taaki head ko hatana ho toh bhi same code chale. "
                "Time hai O of n single pass mein, space O of 1. Do pass wala tareeka pehle length nikaalta hai, phir hatata hai — kaam karta hai, par do baar chalna padta hai."
            ),
            "english": (
                "The pattern is two pointers with a fixed gap. Move the fast pointer n steps ahead, then walk slow and fast together. "
                "When fast reaches the end, slow sits just before the node to remove. Then skip that node. "
                "Use a dummy node so removing the head works with the same code. "
                "Time is O of n in a single pass, space O of 1. The two-pass method first measures the length, then removes — it works, but walks the list twice."
            ),
            "telugu": (
                "Pattern: fixed gap తో two pointers. Fast pointer ని n steps ముందుకు పంపి, తర్వాత slow, fast కలిసి నడపండి. "
                "Fast end కి చేరేసరికి slow తొలగించాల్సిన node కి ముందు ఉంటుంది. Dummy node వాడండి. Time O(n), space O(1), single pass."
            ),
            "tamil": (
                "Pattern: fixed gap உடன் two pointers. Fast pointer-ஐ n steps முன்னே அனுப்பி, பிறகு slow, fast இரண்டையும் சேர்த்து நடத்துங்கள். "
                "Fast end-ஐ அடையும்போது slow நீக்க வேண்டிய node-க்கு முன்னால் இருக்கும். Dummy node பயன்படுத்துங்கள். Time O(n), space O(1), single pass."
            ),
            "kannada": (
                "Pattern: fixed gap ಜೊತೆ two pointers. Fast pointer ಅನ್ನು n steps ಮುಂದಕ್ಕೆ ಕಳುಹಿಸಿ, ನಂತರ slow, fast ಒಟ್ಟಿಗೆ ನಡೆಸಿ. "
                "Fast end ತಲುಪುವಾಗ slow ತೆಗೆದುಹಾಕಬೇಕಾದ node ಗಿಂತ ಮುಂಚೆ ಇರುತ್ತದೆ. Dummy node ಬಳಸಿ. Time O(n), space O(1), single pass."
            ),
            "malayalam": (
                "Pattern: fixed gap-ഓടെ two pointers. Fast pointer n steps മുന്നോട്ട് അയച്ച്, പിന്നീട് slow, fast ഒരുമിച്ച് നടത്തുക. "
                "Fast end-ൽ എത്തുമ്പോൾ slow നീക്കേണ്ട node-ന് തൊട്ടുമുമ്പ് ആയിരിക്കും. Dummy node ഉപയോഗിക്കുക. Time O(n), space O(1), single pass."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: fast ko n aage bhejo, phir dono saath chalo. Fast khatm ho toh slow sahi jagah par hoga.",
            "english": "Simply: send fast n steps ahead, then walk both together. When fast ends, slow is in the right place.",
        },
        "example": "Example: [1,2,3,4,5], n = 2 -> [1,2,3,5]. Node 4 removed.",
    },
    {
        "topic": "Valid Parentheses",
        "category": "Stack & Queue",
        "difficulty": "Easy",
        "keywords": ["valid parentheses", "valid parenthesis", "balanced parentheses", "parentheses valid", "brackets valid", "valid brackets", "balanced brackets"],
        "answers": {
            "hinglish": (
                "Pattern hai stack. Opening bracket mile toh stack mein daalo, closing bracket mile toh stack ka top check karo. "
                "Top par matching opening bracket hai toh pop karo, nahi hai ya stack khaali hai toh galat hai. Aakhir mein stack khaali hona chahiye. "
                "Stack isliye kaam karta hai kyunki bracket last in first out order mein band hote hain, sabse andar wala pehle band hota hai. "
                "Time hai O of n, space O of n worst case mein. Trade-off: sirf ek type ka bracket ho toh counter kaafi hai, lekin teen type ke liye stack chahiye."
            ),
            "english": (
                "The pattern is a stack. On an opening bracket, push it. On a closing bracket, check the top of the stack. "
                "If the top is the matching opener, pop it; if not, or the stack is empty, the string is invalid. At the end the stack must be empty. "
                "A stack works because brackets close last-in-first-out: the innermost closes first. "
                "Time is O of n, space O of n in the worst case. The trade-off: one bracket type needs only a counter, but three types need a stack."
            ),
            "telugu": (
                "Pattern: stack. Opening bracket వస్తే push చేయండి, closing bracket వస్తే stack top check చేయండి. "
                "Matching opener ఉంటే pop చేయండి, లేకపోతే invalid. చివర్లో stack ఖాళీగా ఉండాలి. Time O(n), space O(n). "
                "Brackets last-in-first-out order లో close అవుతాయి, అందుకే stack పనిచేస్తుంది."
            ),
            "tamil": (
                "Pattern: stack. Opening bracket வந்தால் push செய்யுங்கள், closing bracket வந்தால் stack top-ஐ check செய்யுங்கள். "
                "Matching opener இருந்தால் pop செய்யுங்கள், இல்லையெனில் invalid. முடிவில் stack காலியாக இருக்க வேண்டும். Time O(n), space O(n). "
                "Brackets last-in-first-out order-ல் close ஆகும், அதனால் stack வேலை செய்கிறது."
            ),
            "kannada": (
                "Pattern: stack. Opening bracket ಬಂದರೆ push ಮಾಡಿ, closing bracket ಬಂದರೆ stack top check ಮಾಡಿ. "
                "Matching opener ಇದ್ದರೆ pop ಮಾಡಿ, ಇಲ್ಲದಿದ್ದರೆ invalid. ಕೊನೆಯಲ್ಲಿ stack ಖಾಲಿ ಇರಬೇಕು. Time O(n), space O(n). "
                "Brackets last-in-first-out order ನಲ್ಲಿ close ಆಗುತ್ತವೆ, ಆದ್ದರಿಂದ stack ಕೆಲಸ ಮಾಡುತ್ತದೆ."
            ),
            "malayalam": (
                "Pattern: stack. Opening bracket വന്നാൽ push ചെയ്യുക, closing bracket വന്നാൽ stack top check ചെയ്യുക. "
                "Matching opener ഉണ്ടെങ്കിൽ pop ചെയ്യുക, ഇല്ലെങ്കിൽ invalid. അവസാനം stack ശൂന്യമായിരിക്കണം. Time O(n), space O(n). "
                "Brackets last-in-first-out order-ൽ close ആകും, അതുകൊണ്ട് stack പ്രവർത്തിക്കുന്നു."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: kholne wala andar daalo, band karne wala aaye toh upar wala match hona chahiye. Aakhir mein kuch bacha toh galat.",
            "english": "Simply: push openers, and every closer must match the top. Anything left over means invalid.",
        },
        "example": "Example: ()[]{} -> valid. (] -> invalid. ([)] -> invalid.",
    },
    {
        "topic": "Min Stack",
        "category": "Stack & Queue",
        "difficulty": "Medium",
        "keywords": ["min stack", "minimum stack", "stack getmin", "get minimum stack", "minstack"],
        "answers": {
            "hinglish": (
                "Pattern hai do stacks, ya ek stack with pairs. Har push par value ke saath us time tak ka minimum bhi save karo. "
                "Phir getMin sirf top pair ka minimum padh ke O of 1 mein jawab de deta hai. Pop par dono ek saath hat jate hain, toh minimum hamesha sahi rehta hai. "
                "Time hai har operation ke liye O of 1, space O of n extra minimums ke liye. "
                "Trade-off: har push par minimum dobara dhoondhna O of n hota. Thodi extra memory deke hum har operation ko constant time bana lete hain."
            ),
            "english": (
                "The pattern is two stacks, or one stack of pairs. On every push, store the value together with the minimum so far. "
                "Then getMin reads the minimum from the top pair in O of 1. On pop, both leave together, so the minimum stays correct. "
                "Every operation takes O of 1 time, with O of n extra space for the stored minima. "
                "The trade-off: rescanning for the minimum on every push costs O of n. A little extra memory makes every operation constant time."
            ),
            "telugu": (
                "Pattern: రెండు stacks, లేదా pairs తో ఒక stack. ప్రతి push దగ్గర value తో పాటు అప్పటివరకు minimum కూడా save చేయండి. "
                "అప్పుడు getMin O(1) లో answer ఇస్తుంది. ప్రతి operation O(1), space O(n). Minimum మళ్ళీ వెతికితే O(n) పడుతుంది."
            ),
            "tamil": (
                "Pattern: இரண்டு stacks, அல்லது pairs உடன் ஒரு stack. ஒவ்வொரு push-லும் value உடன் அதுவரை minimum-ஐயும் save செய்யுங்கள். "
                "பிறகு getMin O(1)-ல் answer தரும். ஒவ்வொரு operation-ம் O(1), space O(n). Minimum-ஐ மீண்டும் தேடினால் O(n) ஆகும்."
            ),
            "kannada": (
                "Pattern: ಎರಡು stacks, ಅಥವಾ pairs ಜೊತೆ ಒಂದು stack. ಪ್ರತಿ push ನಲ್ಲಿ value ಜೊತೆಗೆ ಅಲ್ಲಿಯವರೆಗಿನ minimum ಅನ್ನು save ಮಾಡಿ. "
                "ನಂತರ getMin O(1) ನಲ್ಲಿ answer ನೀಡುತ್ತದೆ. ಪ್ರತಿ operation O(1), space O(n). Minimum ಅನ್ನು ಮತ್ತೆ ಹುಡುಕಿದರೆ O(n) ಆಗುತ್ತದೆ."
            ),
            "malayalam": (
                "Pattern: രണ്ട് stacks, അല്ലെങ്കിൽ pairs-ഓടെ ഒരു stack. ഓരോ push-ലും value-യോടൊപ്പം അതുവരെയുള്ള minimum-ഉം save ചെയ്യുക. "
                "പിന്നീട് getMin O(1)-ൽ answer തരും. ഓരോ operation-ഉം O(1), space O(n). Minimum വീണ്ടും തിരഞ്ഞാൽ O(n) ആകും."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: har value ke saath us time ka sabse chhota number chipka do. Upar wala chipka number hi minimum hai.",
            "english": "Simply: stick the smallest-so-far number onto every value you push. The top sticker is always the minimum.",
        },
        "example": "Example: push -2, 0, -3. getMin -> -3. pop. top -> 0. getMin -> -2.",
    },
    {
        "topic": "Next Greater Element",
        "category": "Stack & Queue",
        "difficulty": "Medium",
        "keywords": ["next greater element", "next greater", "next largest element", "monotonic stack", "next bigger element"],
        "answers": {
            "hinglish": (
                "Pattern hai monotonic decreasing stack. Array ko right se left scan karo, aur stack mein sirf woh elements rakho jo current se bade hain. "
                "Chhote ya barabar elements ko pop kar do, kyunki woh aage kisi ke liye next greater nahi ban sakte. Stack ka top hi next greater hota hai, khaali hai toh koi nahi. "
                "Har element ek baar push aur ek baar pop hota hai, isliye time O of n hai, space O of n. "
                "Trade-off: har element ke liye aage scan karna O of n square hota hai. Stack se hum bekaar comparisons bacha lete hain."
            ),
            "english": (
                "The pattern is a monotonic decreasing stack. Scan the array from right to left, keeping only elements larger than the current one on the stack. "
                "Pop smaller or equal elements, because they can never be anyone's next greater element. The stack top is the next greater element, or none if empty. "
                "Each element is pushed and popped once, so time is O of n, space O of n. "
                "The trade-off: scanning ahead for every element costs O of n squared. The stack skips comparisons that can never win."
            ),
            "telugu": (
                "Pattern: monotonic decreasing stack. Right నుంచి left కి scan చేయండి, current కన్నా పెద్ద elements మాత్రమే stack లో ఉంచండి. "
                "చిన్న elements ని pop చేయండి. Stack top ఏ next greater element. Time O(n), space O(n). ముందుకు scan చేస్తే O(n square) పడుతుంది."
            ),
            "tamil": (
                "Pattern: monotonic decreasing stack. Right-லிருந்து left-க்கு scan செய்யுங்கள், current-ஐ விட பெரிய elements மட்டும் stack-ல் வையுங்கள். "
                "சிறிய elements-ஐ pop செய்யுங்கள். Stack top தான் next greater element. Time O(n), space O(n). முன்னே scan செய்தால் O(n square) ஆகும்."
            ),
            "kannada": (
                "Pattern: monotonic decreasing stack. Right ನಿಂದ left ಗೆ scan ಮಾಡಿ, current ಗಿಂತ ದೊಡ್ಡ elements ಮಾತ್ರ stack ನಲ್ಲಿ ಇರಿಸಿ. "
                "ಚಿಕ್ಕ elements ಅನ್ನು pop ಮಾಡಿ. Stack top ಏ next greater element. Time O(n), space O(n). ಮುಂದೆ scan ಮಾಡಿದರೆ O(n square) ಆಗುತ್ತದೆ."
            ),
            "malayalam": (
                "Pattern: monotonic decreasing stack. Right-ൽ നിന്ന് left-ലേക്ക് scan ചെയ്യുക, current-നേക്കാൾ വലിയ elements മാത്രം stack-ൽ വയ്ക്കുക. "
                "ചെറിയ elements pop ചെയ്യുക. Stack top ആണ് next greater element. Time O(n), space O(n). മുന്നോട്ട് scan ചെയ്താൽ O(n square) ആകും."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: peeche se aao, chhote elements hata do, upar bacha hua bada wala hi jawab hai.",
            "english": "Simply: walk backwards, throw away smaller elements, and the survivor on top is the answer.",
        },
        "example": "Example: nums = [4,5,2,25] -> next greater = [5,25,25,-1].",
    },
    {
        "topic": "Binary Tree Traversals",
        "category": "Trees",
        "difficulty": "Easy",
        "keywords": ["binary tree traversal", "tree traversal", "inorder", "in order traversal", "preorder", "pre order traversal", "postorder", "post order traversal", "inorder preorder postorder", "traverse tree", "tree traversals"],
        "answers": {
            "hinglish": (
                "Pattern hai recursion: node, left, right ka order badal do, traversal badal jata hai. Inorder hai left, node, right — BST mein ye sorted order deta hai. "
                "Preorder hai node, left, right — tree ko copy karne ya serialize karne mein kaam aata hai. Postorder hai left, right, node — bachchon ko pehle process karna ho toh, jaise delete karte waqt. "
                "Time hai O of n, space O of height recursion stack ke liye. "
                "Trade-off: iterative version stack se bhi likha ja sakta hai, lekin recursion samajhna aur likhna aasan hai. Level order alag hai, woh queue se hota hai, BFS jaisa."
            ),
            "english": (
                "The pattern is recursion: change the order of node, left, and right, and you change the traversal. Inorder is left, node, right — on a BST it gives sorted order. "
                "Preorder is node, left, right — useful for copying or serialising a tree. Postorder is left, right, node — for when children must be processed first, such as deletion. "
                "Time is O of n, space O of height for the recursion stack. "
                "The trade-off: an iterative stack version is possible, but recursion is easier to write and explain. Level order is different: it uses a queue, like BFS."
            ),
            "telugu": (
                "Pattern: recursion — node, left, right order మారిస్తే traversal మారుతుంది. Inorder: left, node, right — BST లో sorted order ఇస్తుంది. "
                "Preorder: node, left, right. Postorder: left, right, node. Time O(n), space O(height). Level order queue తో చేస్తారు, BFS లాగా."
            ),
            "tamil": (
                "Pattern: recursion — node, left, right order-ஐ மாற்றினால் traversal மாறும். Inorder: left, node, right — BST-ல் sorted order தரும். "
                "Preorder: node, left, right. Postorder: left, right, node. Time O(n), space O(height). Level order queue கொண்டு செய்யப்படும், BFS போல."
            ),
            "kannada": (
                "Pattern: recursion — node, left, right order ಬದಲಾಯಿಸಿದರೆ traversal ಬದಲಾಗುತ್ತದೆ. Inorder: left, node, right — BST ನಲ್ಲಿ sorted order ನೀಡುತ್ತದೆ. "
                "Preorder: node, left, right. Postorder: left, right, node. Time O(n), space O(height). Level order queue ಜೊತೆ ಮಾಡುತ್ತಾರೆ, BFS ಹಾಗೆ."
            ),
            "malayalam": (
                "Pattern: recursion — node, left, right order മാറ്റിയാൽ traversal മാറും. Inorder: left, node, right — BST-യിൽ sorted order തരും. "
                "Preorder: node, left, right. Postorder: left, right, node. Time O(n), space O(height). Level order queue കൊണ്ട് ചെയ്യും, BFS പോലെ."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: inorder mein beech wala beech mein, preorder mein pehle, postorder mein aakhir mein. Baaki left phir right.",
            "english": "Simply: inorder puts the node in the middle, preorder first, postorder last. Otherwise left, then right.",
        },
        "example": "Example: tree 1 with left 2 and right 3. Inorder: 2,1,3. Preorder: 1,2,3. Postorder: 2,3,1.",
    },
    {
        "topic": "Maximum Depth of Binary Tree",
        "category": "Trees",
        "difficulty": "Easy",
        "keywords": ["maximum depth of binary tree", "max depth binary tree", "depth of binary tree", "height of binary tree", "tree height", "max depth tree", "tree depth"],
        "answers": {
            "hinglish": (
                "Pattern hai recursion: kisi node ki depth, uske bachchon ki max depth plus one hoti hai. Null node ki depth zero hoti hai. "
                "Left aur right dono ki depth nikaalo, badi wali lo, ek jod do. Yehi soch har node par lagti hai, isliye recursion natural hai. "
                "Time hai O of n, space O of height recursion stack ke liye. Skewed tree mein height n ho sakti hai, balanced mein log n. "
                "Trade-off: iterative BFS level by level bhi kar sakta hai, lekin recursion chhota aur saaf hota hai. Depth aur height mein ek ka farak kabhi kabhi confuse karta hai, definition pehle clear karo."
            ),
            "english": (
                "The pattern is recursion: a node's depth is the maximum depth of its children plus one. A null node's depth is zero. "
                "Compute the depth of the left and right subtrees, take the larger, and add one. The same idea applies at every node, so recursion is natural. "
                "Time is O of n, space O of height for the recursion stack. A skewed tree can have height n; a balanced one, log n. "
                "The trade-off: iterative BFS level by level also works, but recursion is shorter and cleaner. Be clear whether depth counts nodes or edges — definitions differ by one."
            ),
            "telugu": (
                "Pattern: recursion. Node depth = పిల్లల max depth + 1; null node depth 0. Left, right depths తీసుకుని పెద్దదానికి 1 కలపండి. "
                "Time O(n), space O(height). Skewed tree లో height n కావచ్చు, balanced లో log n. BFS తో కూడా చేయవచ్చు, కానీ recursion సులభం."
            ),
            "tamil": (
                "Pattern: recursion. Node depth = குழந்தைகளின் max depth + 1; null node depth 0. Left, right depths எடுத்து பெரியதுடன் 1 சேர்க்கவும். "
                "Time O(n), space O(height). Skewed tree-ல் height n ஆகலாம், balanced-ல் log n. BFS கொண்டும் செய்யலாம், ஆனால் recursion எளிது."
            ),
            "kannada": (
                "Pattern: recursion. Node depth = ಮಕ್ಕಳ max depth + 1; null node depth 0. Left, right depths ತೆಗೆದುಕೊಂಡು ದೊಡ್ಡದಕ್ಕೆ 1 ಸೇರಿಸಿ. "
                "Time O(n), space O(height). Skewed tree ನಲ್ಲಿ height n ಆಗಬಹುದು, balanced ನಲ್ಲಿ log n. BFS ನಿಂದಲೂ ಮಾಡಬಹುದು, ಆದರೆ recursion ಸುಲಭ."
            ),
            "malayalam": (
                "Pattern: recursion. Node depth = കുട്ടികളുടെ max depth + 1; null node depth 0. Left, right depths എടുത്ത് വലുതിനോട് 1 കൂട്ടുക. "
                "Time O(n), space O(height). Skewed tree-യിൽ height n ആകാം, balanced-ൽ log n. BFS കൊണ്ടും ചെയ്യാം, പക്ഷേ recursion എളുപ്പമാണ്."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: neeche kitne level hain, woh gino. Khaali jagah zero, har node ek jod deta hai.",
            "english": "Simply: count the levels below you. Empty is zero, and every node adds one.",
        },
        "example": "Example: root 3, left 9, right 20 with children 15, 7 -> depth = 3.",
    },
    {
        "topic": "Invert Binary Tree",
        "category": "Trees",
        "difficulty": "Easy",
        "keywords": ["invert binary tree", "invert tree", "mirror tree", "mirror binary tree", "flip binary tree", "reverse binary tree"],
        "answers": {
            "hinglish": (
                "Pattern hai recursion with swap. Har node par left aur right bachchon ko swap karo, phir dono par wahi kaam dobara karo. "
                "Null node par ruk jao. Swap pehle karo ya baad mein, dono chalte hain, bas har node par swap hona chahiye. "
                "Time hai O of n, space O of height recursion stack ke liye. "
                "Trade-off: iterative version queue se bhi ho sakta hai, level by level swap karke. Recursion zyada seedha hai aur interview mein pehle yahi bolna chahiye."
            ),
            "english": (
                "The pattern is recursion with a swap. At every node, swap the left and right children, then recurse on both. "
                "Stop at null nodes. Swapping before or after the recursive calls both work, as long as every node is swapped. "
                "Time is O of n, space O of height for the recursion stack. "
                "The trade-off: an iterative queue version can swap level by level. Recursion is more direct and the one to state first in an interview."
            ),
            "telugu": (
                "Pattern: swap తో recursion. ప్రతి node దగ్గర left, right పిల్లల్ని swap చేసి, రెండింటిపై మళ్ళీ అదే చేయండి. Null దగ్గర ఆగండి. "
                "Time O(n), space O(height). Queue తో iterative గా కూడా చేయవచ్చు, కానీ recursion సూటిగా ఉంటుంది."
            ),
            "tamil": (
                "Pattern: swap உடன் recursion. ஒவ்வொரு node-லும் left, right குழந்தைகளை swap செய்து, இரண்டிலும் மீண்டும் அதையே செய்யுங்கள். Null-ல் நிறுத்துங்கள். "
                "Time O(n), space O(height). Queue கொண்டு iterative ஆகவும் செய்யலாம், ஆனால் recursion நேரடியானது."
            ),
            "kannada": (
                "Pattern: swap ಜೊತೆ recursion. ಪ್ರತಿ node ನಲ್ಲಿ left, right ಮಕ್ಕಳನ್ನು swap ಮಾಡಿ, ಎರಡರ ಮೇಲೂ ಮತ್ತೆ ಅದನ್ನೇ ಮಾಡಿ. Null ನಲ್ಲಿ ನಿಲ್ಲಿ. "
                "Time O(n), space O(height). Queue ಜೊತೆ iterative ಆಗಿಯೂ ಮಾಡಬಹುದು, ಆದರೆ recursion ನೇರವಾಗಿದೆ."
            ),
            "malayalam": (
                "Pattern: swap-ഓടെ recursion. ഓരോ node-ലും left, right കുട്ടികളെ swap ചെയ്ത്, രണ്ടിലും വീണ്ടും അതുതന്നെ ചെയ്യുക. Null-ൽ നിർത്തുക. "
                "Time O(n), space O(height). Queue കൊണ്ട് iterative ആയും ചെയ്യാം, പക്ഷേ recursion നേരിട്ടുള്ളതാണ്."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: har node ke left right badal do, sheesha image ban jayegi.",
            "english": "Simply: swap left and right at every node, and you get the mirror image.",
        },
        "example": "Example: [4,2,7,1,3,6,9] inverted -> [4,7,2,9,6,3,1].",
    },
    {
        "topic": "Validate Binary Search Tree",
        "category": "Trees",
        "difficulty": "Medium",
        "keywords": ["validate binary search tree", "validate bst", "check bst", "is valid bst", "valid bst", "bst valid", "binary search tree valid"],
        "answers": {
            "hinglish": (
                "Pattern hai range check with recursion. Har node ke liye ek allowed range rakho, low aur high. Node ki value range ke andar honi chahiye. "
                "Left mein jao toh high node ki value ban jati hai, right mein jao toh low node ki value ban jati hai. Sirf direct bachchon ko dekhna kaafi nahi hai, poore subtree ko range mein rehna hai. "
                "Time hai O of n, space O of height. Trade-off: inorder traversal karke sorted hai ya nahi check karna bhi chalta hai, lekin range wala tareeka galat node milte hi ruk sakta hai. "
                "Edge case: duplicate values allowed nahi hain, strict less than aur greater than use karo."
            ),
            "english": (
                "The pattern is a range check with recursion. Carry an allowed range, low and high, for each node. The node's value must lie inside it. "
                "Going left, high becomes the node's value; going right, low becomes the node's value. Checking only direct children is not enough — the whole subtree must respect the range. "
                "Time is O of n, space O of height. The trade-off: an inorder traversal that checks sorted order also works, but the range method can stop at the first violation. "
                "Edge case: duplicates are not allowed, so use strict less-than and greater-than."
            ),
            "telugu": (
                "Pattern: range check తో recursion. ప్రతి node కి low, high range ఉంచండి; value range లోపల ఉండాలి. Left కి వెళ్తే high = node value, "
                "right కి వెళ్తే low = node value. పిల్లల్ని మాత్రమే చూడటం సరిపోదు. Time O(n), space O(height). Duplicates allowed కావు."
            ),
            "tamil": (
                "Pattern: range check உடன் recursion. ஒவ்வொரு node-க்கும் low, high range வையுங்கள்; value range-க்குள் இருக்க வேண்டும். Left சென்றால் high = node value, "
                "right சென்றால் low = node value. குழந்தைகளை மட்டும் பார்ப்பது போதாது. Time O(n), space O(height). Duplicates அனுமதிக்கப்படவில்லை."
            ),
            "kannada": (
                "Pattern: range check ಜೊತೆ recursion. ಪ್ರತಿ node ಗೆ low, high range ಇರಿಸಿ; value range ಒಳಗೆ ಇರಬೇಕು. Left ಗೆ ಹೋದರೆ high = node value, "
                "right ಗೆ ಹೋದರೆ low = node value. ಮಕ್ಕಳನ್ನು ಮಾತ್ರ ನೋಡುವುದು ಸಾಕಾಗುವುದಿಲ್ಲ. Time O(n), space O(height). Duplicates allowed ಅಲ್ಲ."
            ),
            "malayalam": (
                "Pattern: range check-ഓടെ recursion. ഓരോ node-നും low, high range വയ്ക്കുക; value range-നുള്ളിൽ ആയിരിക്കണം. Left-ലേക്ക് പോയാൽ high = node value, "
                "right-ലേക്ക് പോയാൽ low = node value. കുട്ടികളെ മാത്രം നോക്കിയാൽ പോരാ. Time O(n), space O(height). Duplicates അനുവദനീയമല്ല."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: har node ko apni had mein rehna hai. Baayein wale chhote, daayein wale bade, poori shaka tak.",
            "english": "Simply: every node must stay within its bounds. Everything left is smaller, everything right is bigger, all the way down.",
        },
        "example": "Example: [2,1,3] -> valid. [5,1,4,null,null,3,6] -> invalid, 3 is in the right subtree of 5 but smaller than 5.",
    },
    {
        "topic": "Lowest Common Ancestor of a BST",
        "category": "Trees",
        "difficulty": "Medium",
        "keywords": ["lowest common ancestor", "lca", "lowest common ancestor bst", "lca bst", "common ancestor", "lowest common ancestor binary search tree"],
        "answers": {
            "hinglish": (
                "Pattern hai BST property ka use. Root se shuru karo. Dono nodes root se chhote hain toh answer left mein hai, dono bade hain toh right mein hai. "
                "Ek chhota ek bada hai, ya ek root ke barabar hai, toh wahi root answer hai, kyunki wahan paths alag hote hain. "
                "Time hai O of height, space O of 1 iterative version mein. "
                "Trade-off: general binary tree mein ye trick nahi chalti, wahan dono taraf search karke recursion se karna padta hai. BST mein ordering hi shortcut hai, use bolna important hai."
            ),
            "english": (
                "The pattern is to use the BST property. Start at the root. If both nodes are smaller than the root, the answer is on the left; if both are larger, on the right. "
                "If one is smaller and one larger, or one equals the root, that root is the answer, because the paths split there. "
                "Time is O of height, space O of 1 for the iterative version. "
                "The trade-off: this trick does not work for a general binary tree, where you must search both sides recursively. In a BST, the ordering is the shortcut — say so in the interview."
            ),
            "telugu": (
                "Pattern: BST property వాడండి. Root నుంచి మొదలుపెట్టండి. రెండు nodes root కన్నా చిన్నవైతే left, పెద్దవైతే right. "
                "ఒకటి చిన్నది, ఒకటి పెద్దది అయితే ఆ root ఏ answer. Time O(height), space O(1). General binary tree లో ఈ trick పనిచేయదు."
            ),
            "tamil": (
                "Pattern: BST property-ஐ பயன்படுத்துங்கள். Root-லிருந்து தொடங்குங்கள். இரண்டு nodes-ம் root-ஐ விட சிறியதாக இருந்தால் left, பெரியதாக இருந்தால் right. "
                "ஒன்று சிறியது, ஒன்று பெரியது என்றால் அந்த root தான் answer. Time O(height), space O(1). General binary tree-ல் இந்த trick வேலை செய்யாது."
            ),
            "kannada": (
                "Pattern: BST property ಬಳಸಿ. Root ನಿಂದ ಶುರು ಮಾಡಿ. ಎರಡೂ nodes root ಗಿಂತ ಚಿಕ್ಕದಾಗಿದ್ದರೆ left, ದೊಡ್ಡದಾಗಿದ್ದರೆ right. "
                "ಒಂದು ಚಿಕ್ಕದು, ಒಂದು ದೊಡ್ಡದು ಆದರೆ ಆ root ಏ answer. Time O(height), space O(1). General binary tree ನಲ್ಲಿ ಈ trick ಕೆಲಸ ಮಾಡುವುದಿಲ್ಲ."
            ),
            "malayalam": (
                "Pattern: BST property ഉപയോഗിക്കുക. Root-ൽ നിന്ന് തുടങ്ങുക. രണ്ട് nodes-ഉം root-നേക്കാൾ ചെറുതാണെങ്കിൽ left, വലുതാണെങ്കിൽ right. "
                "ഒന്ന് ചെറുത്, ഒന്ന് വലുത് ആണെങ്കിൽ ആ root ആണ് answer. Time O(height), space O(1). General binary tree-യിൽ ഈ trick പ്രവർത്തിക്കില്ല."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: jahan dono ke raaste alag hote hain, wahi common ancestor hai.",
            "english": "Simply: the ancestor where the two paths split is the answer.",
        },
        "example": "Example: BST [6,2,8,0,4,7,9], p = 2, q = 8 -> LCA = 6. p = 2, q = 4 -> LCA = 2.",
    },
    {
        "topic": "Breadth-First Search (BFS)",
        "category": "Graphs",
        "difficulty": "Medium",
        "keywords": ["breadth first search", "bfs", "breadth-first", "bfs graph", "breadth first traversal", "level order graph"],
        "answers": {
            "hinglish": (
                "Pattern hai queue with visited set. Start node ko queue mein daalo aur visited mark karo. Queue se node nikaalo, uske neighbours ko dekho, "
                "jo visited nahi hain unhe queue mein daalo aur visited mark karo. Ye level by level chalta hai, pehle paas wale, phir door wale. "
                "Isliye BFS unweighted graph mein shortest path, matlab sabse kam edges, deta hai. "
                "Time hai O of vertices plus edges, space O of vertices. Trade-off: DFS se zyada memory leta hai kyunki poora level queue mein rehta hai, lekin shortest path ki guarantee deta hai."
            ),
            "english": (
                "The pattern is a queue with a visited set. Put the start node in the queue and mark it visited. Remove a node, look at its neighbours, "
                "and enqueue any unvisited ones, marking them visited. This runs level by level: near nodes first, then farther ones. "
                "That is why BFS gives the shortest path, fewest edges, in an unweighted graph. "
                "Time is O of vertices plus edges, space O of vertices. The trade-off: it uses more memory than DFS because a whole level sits in the queue, but it guarantees the shortest path."
            ),
            "telugu": (
                "Pattern: visited set తో queue. Start node ని queue లో వేసి visited mark చేయండి. Node తీసి, neighbours చూసి, "
                "visited కానివాటిని queue లో వేయండి. Level by level వెళ్తుంది, అందుకే unweighted graph లో shortest path ఇస్తుంది. Time O(V + E), space O(V)."
            ),
            "tamil": (
                "Pattern: visited set உடன் queue. Start node-ஐ queue-ல் போட்டு visited mark செய்யுங்கள். Node-ஐ எடுத்து, neighbours-ஐ பார்த்து, "
                "visited ஆகாதவற்றை queue-ல் போடுங்கள். Level by level செல்லும், அதனால் unweighted graph-ல் shortest path தரும். Time O(V + E), space O(V)."
            ),
            "kannada": (
                "Pattern: visited set ಜೊತೆ queue. Start node ಅನ್ನು queue ನಲ್ಲಿ ಹಾಕಿ visited mark ಮಾಡಿ. Node ತೆಗೆದು, neighbours ನೋಡಿ, "
                "visited ಆಗದವುಗಳನ್ನು queue ನಲ್ಲಿ ಹಾಕಿ. Level by level ಹೋಗುತ್ತದೆ, ಆದ್ದರಿಂದ unweighted graph ನಲ್ಲಿ shortest path ನೀಡುತ್ತದೆ. Time O(V + E), space O(V)."
            ),
            "malayalam": (
                "Pattern: visited set-ഓടെ queue. Start node queue-ൽ ഇട്ട് visited mark ചെയ്യുക. Node എടുത്ത്, neighbours നോക്കി, "
                "visited ആകാത്തവ queue-ൽ ഇടുക. Level by level പോകും, അതുകൊണ്ട് unweighted graph-ൽ shortest path തരും. Time O(V + E), space O(V)."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: pehle paas wale, phir unke paas wale. Jaise paani mein lehar failti hai.",
            "english": "Simply: near neighbours first, then their neighbours — like ripples spreading in water.",
        },
        "example": "Example: graph 1 connected to 2 and 3, 2 connected to 4. BFS from 1 visits 1, 2, 3, then 4.",
    },
    {
        "topic": "Depth-First Search (DFS)",
        "category": "Graphs",
        "difficulty": "Medium",
        "keywords": ["depth first search", "dfs", "depth-first", "dfs graph", "depth first traversal"],
        "answers": {
            "hinglish": (
                "Pattern hai recursion ya stack with visited set. Ek path par jitna gehra ja sakte ho jao, phir peeche aao aur doosra path try karo. "
                "Visited set zaroori hai, nahi toh cycle mein ghoomte rahoge. DFS cycle detect karne, connected components ginne, aur topological sort jaise kaamon mein kaam aata hai. "
                "Time hai O of vertices plus edges, space O of vertices recursion stack ke liye. "
                "Trade-off: DFS shortest path ki guarantee nahi deta, woh BFS ka kaam hai. Lekin DFS kam memory mein chalta hai aur backtracking wale problems mein natural hai."
            ),
            "english": (
                "The pattern is recursion or a stack with a visited set. Go as deep as you can along one path, then backtrack and try another. "
                "A visited set is essential, or you will loop forever in a cycle. DFS is used for cycle detection, counting connected components, and topological sort. "
                "Time is O of vertices plus edges, space O of vertices for the recursion stack. "
                "The trade-off: DFS does not guarantee the shortest path — that is BFS's job. But DFS uses less memory and feels natural for backtracking problems."
            ),
            "telugu": (
                "Pattern: visited set తో recursion లేదా stack. ఒక path లో వీలైనంత లోతుగా వెళ్లి, వెనక్కి వచ్చి మరో path try చేయండి. "
                "Cycle detection, connected components కి ఉపయోగపడుతుంది. Time O(V + E), space O(V). Shortest path guarantee ఇవ్వదు — అది BFS పని."
            ),
            "tamil": (
                "Pattern: visited set உடன் recursion அல்லது stack. ஒரு path-ல் முடிந்தவரை ஆழமாகச் சென்று, பின்னே வந்து வேறு path try செய்யுங்கள். "
                "Cycle detection, connected components-க்கு பயன்படும். Time O(V + E), space O(V). Shortest path guarantee தராது — அது BFS வேலை."
            ),
            "kannada": (
                "Pattern: visited set ಜೊತೆ recursion ಅಥವಾ stack. ಒಂದು path ನಲ್ಲಿ ಸಾಧ್ಯವಾದಷ್ಟು ಆಳಕ್ಕೆ ಹೋಗಿ, ಹಿಂದಕ್ಕೆ ಬಂದು ಇನ್ನೊಂದು path try ಮಾಡಿ. "
                "Cycle detection, connected components ಗೆ ಉಪಯುಕ್ತ. Time O(V + E), space O(V). Shortest path guarantee ನೀಡುವುದಿಲ್ಲ — ಅದು BFS ಕೆಲಸ."
            ),
            "malayalam": (
                "Pattern: visited set-ഓടെ recursion അല്ലെങ്കിൽ stack. ഒരു path-ൽ കഴിയുന്നത്ര ആഴത്തിൽ പോയി, തിരികെ വന്ന് മറ്റൊരു path try ചെയ്യുക. "
                "Cycle detection, connected components എന്നിവയ്ക്ക് ഉപയോഗപ്രദം. Time O(V + E), space O(V). Shortest path guarantee തരില്ല — അത് BFS-ന്റെ ജോലിയാണ്."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: ek raaste par aakhir tak jao, phir wapas aake doosra raasta lo. Gaye hue jagah par dobara mat jao.",
            "english": "Simply: follow one road to its end, backtrack, and try the next road. Never revisit a place you have seen.",
        },
        "example": "Example: graph 1 connected to 2 and 3, 2 connected to 4. DFS from 1 can visit 1, 2, 4, then 3.",
    },
    {
        "topic": "Number of Islands",
        "category": "Graphs",
        "difficulty": "Medium",
        "keywords": ["number of islands", "islands", "count islands", "number islands", "island count", "connected islands"],
        "answers": {
            "hinglish": (
                "Pattern hai grid DFS or BFS with visited marking. Grid ke har cell par jao. Agar cell land hai aur visited nahi hai, toh count ek badhao aur us poore island ko flood fill se visited mark kar do. "
                "Flood fill matlab upar neeche baayein daayein ke land cells ko bhi visited karna, jab tak island khatm na ho. Diagonal count nahi hota, sirf chaar disha. "
                "Time hai O of rows into columns, space O of rows into columns worst case recursion ke liye. "
                "Trade-off: grid ko hi visited mark karke badalna space bachata hai, lekin input badal deta hai. Alag visited set input ko safe rakhta hai, par extra memory leta hai."
            ),
            "english": (
                "The pattern is grid DFS or BFS with visited marking. Scan every cell. If a cell is land and unvisited, increase the count and flood-fill the whole island as visited. "
                "Flood fill means marking the land cells up, down, left, and right, until the island ends. Diagonals do not count, only four directions. "
                "Time is O of rows times columns, space O of rows times columns in the worst case for recursion. "
                "The trade-off: marking the grid itself saves space but mutates the input. A separate visited set keeps the input safe but costs extra memory."
            ),
            "telugu": (
                "Pattern: visited marking తో grid DFS లేదా BFS. ప్రతి cell చూడండి; land అయి, visited కాకపోతే count పెంచి, ఆ island మొత్తం flood fill చేయండి. "
                "నాలుగు దిశలు మాత్రమే — diagonal లెక్కలోకి రాదు. Time O(rows x cols). Grid నే mark చేస్తే space ఆదా, కానీ input మారిపోతుంది."
            ),
            "tamil": (
                "Pattern: visited marking உடன் grid DFS அல்லது BFS. ஒவ்வொரு cell-ஐயும் பாருங்கள்; land ஆகவும் visited ஆகாமலும் இருந்தால் count-ஐ அதிகரித்து, அந்த island முழுவதையும் flood fill செய்யுங்கள். "
                "நான்கு திசைகள் மட்டும் — diagonal கணக்கில் வராது. Time O(rows x cols). Grid-ஐயே mark செய்தால் space மிச்சம், ஆனால் input மாறிவிடும்."
            ),
            "kannada": (
                "Pattern: visited marking ಜೊತೆ grid DFS ಅಥವಾ BFS. ಪ್ರತಿ cell ನೋಡಿ; land ಆಗಿ, visited ಆಗದಿದ್ದರೆ count ಹೆಚ್ಚಿಸಿ, ಆ island ಪೂರ್ತಿ flood fill ಮಾಡಿ. "
                "ನಾಲ್ಕು ದಿಕ್ಕುಗಳು ಮಾತ್ರ — diagonal ಲೆಕ್ಕಕ್ಕೆ ಬರುವುದಿಲ್ಲ. Time O(rows x cols). Grid ಅನ್ನು mark ಮಾಡಿದರೆ space ಉಳಿಯುತ್ತದೆ, ಆದರೆ input ಬದಲಾಗುತ್ತದೆ."
            ),
            "malayalam": (
                "Pattern: visited marking-ഓടെ grid DFS അല്ലെങ്കിൽ BFS. ഓരോ cell-ഉം നോക്കുക; land ആയും visited ആകാതെയും ആണെങ്കിൽ count കൂട്ടി, ആ island മുഴുവൻ flood fill ചെയ്യുക. "
                "നാല് ദിശകൾ മാത്രം — diagonal കണക്കിൽ വരില്ല. Time O(rows x cols). Grid തന്നെ mark ചെയ്താൽ space ലാഭം, പക്ഷേ input മാറും."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: naya land mila toh ek island gino, phir usse jude saare land ko rang do taaki dobara na gino.",
            "english": "Simply: when you find fresh land, count one island, then paint the whole connected patch so you never count it twice.",
        },
        "example": "Example: grid [[1,1,0],[1,0,0],[0,0,1]] -> 2 islands.",
    },
    {
        "topic": "Climbing Stairs",
        "category": "Dynamic Programming",
        "difficulty": "Easy",
        "keywords": ["climbing stairs", "climb stairs", "stairs", "climbing staircase", "ways to climb stairs"],
        "answers": {
            "hinglish": (
                "Pattern hai dynamic programming with Fibonacci recurrence. Nth step tak pahunchne ke tareeke, n minus 1 se ek step aur n minus 2 se do step ke tareekon ka sum hote hain. "
                "Matlab dp of n equals dp of n minus 1 plus dp of n minus 2. Sirf pichhle do values chahiye, isliye do variables kaafi hain. "
                "Time hai O of n, space O of 1. Trade-off: plain recursion bina memo ke exponential hoti hai, kyunki wahi subproblems baar baar solve hote hain. "
                "DP mein har subproblem ek baar solve hota hai. Ye DP samajhne ka sabse aasan pehla problem hai."
            ),
            "english": (
                "The pattern is dynamic programming with a Fibonacci recurrence. The ways to reach step n equal the ways to reach n minus 1 plus the ways to reach n minus 2. "
                "That is, dp of n equals dp of n minus 1 plus dp of n minus 2. Only the last two values are needed, so two variables are enough. "
                "Time is O of n, space O of 1. The trade-off: plain recursion without memoisation is exponential, because the same subproblems are solved again and again. "
                "With DP, each subproblem is solved once. This is the easiest first DP problem."
            ),
            "telugu": (
                "Pattern: Fibonacci recurrence తో DP. dp(n) = dp(n-1) + dp(n-2). గత రెండు values మాత్రమే కావాలి, అందుకే రెండు variables చాలు. "
                "Time O(n), space O(1). Memo లేని recursion exponential అవుతుంది — అదే subproblems మళ్ళీ మళ్ళీ solve అవుతాయి. DP లో ప్రతిదీ ఒక్కసారే."
            ),
            "tamil": (
                "Pattern: Fibonacci recurrence உடன் DP. dp(n) = dp(n-1) + dp(n-2). கடைசி இரண்டு values மட்டும் போதும், அதனால் இரண்டு variables போதும். "
                "Time O(n), space O(1). Memo இல்லாத recursion exponential ஆகும் — அதே subproblems மீண்டும் மீண்டும் solve ஆகும். DP-ல் ஒவ்வொன்றும் ஒரு முறைதான்."
            ),
            "kannada": (
                "Pattern: Fibonacci recurrence ಜೊತೆ DP. dp(n) = dp(n-1) + dp(n-2). ಕೊನೆಯ ಎರಡು values ಮಾತ್ರ ಬೇಕು, ಆದ್ದರಿಂದ ಎರಡು variables ಸಾಕು. "
                "Time O(n), space O(1). Memo ಇಲ್ಲದ recursion exponential ಆಗುತ್ತದೆ — ಅದೇ subproblems ಮತ್ತೆ ಮತ್ತೆ solve ಆಗುತ್ತವೆ. DP ನಲ್ಲಿ ಪ್ರತಿಯೊಂದೂ ಒಮ್ಮೆ ಮಾತ್ರ."
            ),
            "malayalam": (
                "Pattern: Fibonacci recurrence-ഓടെ DP. dp(n) = dp(n-1) + dp(n-2). അവസാന രണ്ട് values മാത്രം മതി, അതുകൊണ്ട് രണ്ട് variables മതി. "
                "Time O(n), space O(1). Memo ഇല്ലാത്ത recursion exponential ആകും — അതേ subproblems വീണ്ടും വീണ്ടും solve ആകും. DP-യിൽ ഓരോന്നും ഒരിക്കൽ മാത്രം."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: aakhri step par do taraf se aa sakte ho, ek peeche se ya do peeche se. Dono ke tareeke jod do.",
            "english": "Simply: you can arrive at the last step from one step back or two steps back. Add those two counts.",
        },
        "example": "Example: n = 2 -> 2 ways (1+1, 2). n = 3 -> 3 ways (1+1+1, 1+2, 2+1).",
    },
    {
        "topic": "House Robber",
        "category": "Dynamic Programming",
        "difficulty": "Medium",
        "keywords": ["house robber", "house robbery", "rob houses", "robber", "maximum loot houses"],
        "answers": {
            "hinglish": (
                "Pattern hai DP with take or skip. Har ghar par do choice hain: is ghar ko looto aur pichhle ghar ko chhodo, ya is ghar ko chhodo aur pichhle tak ka best lo. "
                "Matlab dp of i equals max of dp of i minus 1, aur dp of i minus 2 plus current value. Sirf pichhle do values chahiye. "
                "Time hai O of n, space O of 1. Trade-off: har combination try karna exponential hota hai. DP mein decision sirf pichhle do gharon par depend karta hai, isliye ek pass kaafi hai. "
                "Interview mein ye batana zaroori hai ki paas paas wale ghar lootna mana hai, wahi constraint recurrence banata hai."
            ),
            "english": (
                "The pattern is DP with take or skip. At each house you have two choices: rob this house and skip the previous one, or skip this house and keep the previous best. "
                "So dp of i equals the max of dp of i minus 1, and dp of i minus 2 plus the current value. Only the last two values are needed. "
                "Time is O of n, space O of 1. The trade-off: trying every combination is exponential. In DP, each decision depends only on the previous two houses, so one pass is enough. "
                "In an interview, state the constraint clearly: adjacent houses cannot both be robbed — that constraint creates the recurrence."
            ),
            "telugu": (
                "Pattern: take or skip తో DP. ప్రతి ఇంటి దగ్గర రెండు choices: ఈ ఇల్లు దోచుకుని ముందు ఇల్లు వదలడం, లేదా ఈ ఇల్లు వదిలి ముందు best తీసుకోవడం. "
                "dp(i) = max(dp(i-1), dp(i-2) + value). Time O(n), space O(1). పక్కపక్క ఇళ్ళు రెండూ దోచుకోకూడదు — అదే constraint."
            ),
            "tamil": (
                "Pattern: take or skip உடன் DP. ஒவ்வொரு வீட்டிலும் இரண்டு choices: இந்த வீட்டை கொள்ளையடித்து முந்தைய வீட்டை விடுவது, அல்லது இந்த வீட்டை விட்டு முந்தைய best-ஐ எடுப்பது. "
                "dp(i) = max(dp(i-1), dp(i-2) + value). Time O(n), space O(1). பக்கத்து வீடுகள் இரண்டையும் கொள்ளையடிக்க முடியாது — அதுதான் constraint."
            ),
            "kannada": (
                "Pattern: take or skip ಜೊತೆ DP. ಪ್ರತಿ ಮನೆಯಲ್ಲಿ ಎರಡು choices: ಈ ಮನೆಯನ್ನು ದೋಚಿ ಹಿಂದಿನ ಮನೆಯನ್ನು ಬಿಡುವುದು, ಅಥವಾ ಈ ಮನೆಯನ್ನು ಬಿಟ್ಟು ಹಿಂದಿನ best ತೆಗೆದುಕೊಳ್ಳುವುದು. "
                "dp(i) = max(dp(i-1), dp(i-2) + value). Time O(n), space O(1). ಪಕ್ಕಪಕ್ಕದ ಮನೆಗಳೆರಡನ್ನೂ ದೋಚುವಂತಿಲ್ಲ — ಅದೇ constraint."
            ),
            "malayalam": (
                "Pattern: take or skip-ഓടെ DP. ഓരോ വീട്ടിലും രണ്ട് choices: ഈ വീട് കൊള്ളയടിച്ച് മുൻ വീട് വിടുക, അല്ലെങ്കിൽ ഈ വീട് വിട്ട് മുൻ best എടുക്കുക. "
                "dp(i) = max(dp(i-1), dp(i-2) + value). Time O(n), space O(1). അടുത്തടുത്ത വീടുകൾ രണ്ടും കൊള്ളയടിക്കാൻ പാടില്ല — അതാണ് constraint."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: har ghar par socho, lootoon ya chhodoon. Lootna hai toh pichhla chhodo, nahi toh pichhla best le lo.",
            "english": "Simply: at each house, rob it and skip the last, or skip it and keep the last best. Take whichever is bigger.",
        },
        "example": "Example: nums = [2,7,9,3,1] -> rob houses 2, 9, 1 = 12.",
    },
    {
        "topic": "Coin Change",
        "category": "Dynamic Programming",
        "difficulty": "Medium",
        "keywords": ["coin change", "coinchange", "minimum coins", "fewest coins", "change coins"],
        "answers": {
            "hinglish": (
                "Pattern hai DP over amount. Har amount ke liye minimum coins nikaalo, har coin ko aakhri coin maan ke. "
                "Matlab dp of amount equals one plus minimum of dp of amount minus coin, saare coins ke liye. Base case dp zero equals zero hai, impossible amounts ko infinity rakho. "
                "Time hai O of amount into number of coins, space O of amount. "
                "Trade-off: greedy, matlab hamesha sabse bada coin lena, har coin system mein kaam nahi karta. DP har coin system mein sahi jawab deta hai, bas table bharna padta hai."
            ),
            "english": (
                "The pattern is DP over the amount. For each amount, find the minimum coins by trying every coin as the last coin. "
                "So dp of amount equals one plus the minimum of dp of amount minus coin, over all coins. The base case is dp of zero equals zero, and impossible amounts stay at infinity. "
                "Time is O of amount times number of coins, space O of amount. "
                "The trade-off: greedy, always taking the largest coin, fails for some coin systems. DP gives the right answer for any coin system, at the cost of filling a table."
            ),
            "telugu": (
                "Pattern: amount పై DP. ప్రతి amount కి, ప్రతి coin ని చివరి coin గా try చేసి minimum coins కనుగొనండి. "
                "dp(amount) = 1 + min(dp(amount - coin)). Time O(amount x coins), space O(amount). Greedy అన్ని coin systems లో పనిచేయదు; DP ఎప్పుడూ సరైన answer ఇస్తుంది."
            ),
            "tamil": (
                "Pattern: amount மீது DP. ஒவ்வொரு amount-க்கும், ஒவ்வொரு coin-ஐயும் கடைசி coin ஆக try செய்து minimum coins கண்டறியுங்கள். "
                "dp(amount) = 1 + min(dp(amount - coin)). Time O(amount x coins), space O(amount). Greedy எல்லா coin systems-லும் வேலை செய்யாது; DP எப்போதும் சரியான answer தரும்."
            ),
            "kannada": (
                "Pattern: amount ಮೇಲೆ DP. ಪ್ರತಿ amount ಗೆ, ಪ್ರತಿ coin ಅನ್ನು ಕೊನೆಯ coin ಆಗಿ try ಮಾಡಿ minimum coins ಕಂಡುಹಿಡಿಯಿರಿ. "
                "dp(amount) = 1 + min(dp(amount - coin)). Time O(amount x coins), space O(amount). Greedy ಎಲ್ಲಾ coin systems ನಲ್ಲಿ ಕೆಲಸ ಮಾಡುವುದಿಲ್ಲ; DP ಯಾವಾಗಲೂ ಸರಿಯಾದ answer ನೀಡುತ್ತದೆ."
            ),
            "malayalam": (
                "Pattern: amount-ന് മുകളിൽ DP. ഓരോ amount-നും, ഓരോ coin-നെയും അവസാന coin ആയി try ചെയ്ത് minimum coins കണ്ടെത്തുക. "
                "dp(amount) = 1 + min(dp(amount - coin)). Time O(amount x coins), space O(amount). Greedy എല്ലാ coin systems-ലും പ്രവർത്തിക്കില്ല; DP എപ്പോഴും ശരിയായ answer തരും."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: chhote amount se shuru karo, har amount ke liye har coin try karo, sabse kam coins wala jawab rakho.",
            "english": "Simply: build up from small amounts, try every coin for each amount, and keep the fewest coins.",
        },
        "example": "Example: coins = [1,2,5], amount = 11 -> 3 coins (5+5+1). Amount = 3, coins = [2] -> impossible, -1.",
    },
    {
        "topic": "Quick Sort",
        "category": "Sorting",
        "difficulty": "Medium",
        "keywords": ["quick sort", "quicksort", "quick-sort", "partition sort", "quicksort algorithm", "क्विक सॉर्ट", "క్విక్ సార్ట్", "குயிக் சார்ட்", "ಕ್ವಿಕ್ ಸಾರ್ಟ್", "ക്വിക്ക് സോർട്ട്"],
        "answers": {
            "hinglish": (
                "Pattern hai divide and conquer with partition. Ek pivot chuno, array ko rearrange karo taaki pivot se chhote elements baayein aur bade daayein aa jayein. "
                "Phir dono halves par wahi kaam dobara karo. Partition hi asli kaam hai, baaki recursion hai. "
                "Average time hai O of n log n, worst case O of n square jab pivot hamesha sabse chhota ya sabse bada ho, jaise sorted array mein pehla element pivot ho. "
                "Space hai O of log n recursion stack ke liye. Trade-off: merge sort se tez hota hai practice mein aur in place hota hai, lekin stable nahi hai aur worst case bura ho sakta hai. Random pivot worst case se bachata hai."
            ),
            "english": (
                "The pattern is divide and conquer with partitioning. Pick a pivot, rearrange the array so smaller elements go left and larger ones go right. "
                "Then repeat on both halves. Partitioning is the real work; the rest is recursion. "
                "Average time is O of n log n, worst case O of n squared when the pivot is always the smallest or largest, such as the first element of a sorted array. "
                "Space is O of log n for the recursion stack. The trade-off: it is fast in practice and in place, but not stable, and the worst case is bad. A random pivot avoids the worst case."
            ),
            "telugu": (
                "Pattern: partition తో divide and conquer. Pivot ఎంచుకుని, చిన్న elements ఎడమ, పెద్ద elements కుడి వైపు వచ్చేలా rearrange చేయండి, "
                "తర్వాత రెండు halves పై మళ్ళీ చేయండి. Average time O(n log n), worst case O(n square). Space O(log n). Random pivot worst case నుంచి కాపాడుతుంది."
            ),
            "tamil": (
                "Pattern: partition உடன் divide and conquer. Pivot தேர்ந்து, சிறிய elements இடது, பெரிய elements வலது பக்கம் வருமாறு rearrange செய்யுங்கள், "
                "பிறகு இரண்டு halves-லும் மீண்டும் செய்யுங்கள். Average time O(n log n), worst case O(n square). Space O(log n). Random pivot worst case-லிருந்து காக்கும்."
            ),
            "kannada": (
                "Pattern: partition ಜೊತೆ divide and conquer. Pivot ಆರಿಸಿ, ಚಿಕ್ಕ elements ಎಡ, ದೊಡ್ಡ elements ಬಲ ಬದಿಗೆ ಬರುವಂತೆ rearrange ಮಾಡಿ, "
                "ನಂತರ ಎರಡು halves ಮೇಲೆ ಮತ್ತೆ ಮಾಡಿ. Average time O(n log n), worst case O(n square). Space O(log n). Random pivot worst case ನಿಂದ ಕಾಪಾಡುತ್ತದೆ."
            ),
            "malayalam": (
                "Pattern: partition-ഓടെ divide and conquer. Pivot തിരഞ്ഞെടുത്ത്, ചെറിയ elements ഇടത്, വലിയ elements വലത് വശത്ത് വരുംവിധം rearrange ചെയ്യുക, "
                "പിന്നീട് രണ്ട് halves-ലും വീണ്ടും ചെയ്യുക. Average time O(n log n), worst case O(n square). Space O(log n). Random pivot worst case-ൽ നിന്ന് രക്ഷിക്കും."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: ek pivot lo, chhote baayein, bade daayein, phir dono taraf wahi karo.",
            "english": "Simply: pick a pivot, put smaller elements left and larger right, then do the same on both sides.",
        },
        "example": "Example: [3,6,8,10,1,2,1] with pivot 3 -> left [1,2,1], pivot 3, right [6,8,10], then sort each side.",
    },
    {
        "topic": "Merge Sort",
        "category": "Sorting",
        "difficulty": "Medium",
        "keywords": ["merge sort", "mergesort", "merge-sort", "merge sort algorithm", "मर्ज सॉर्ट", "మెర్జ్ సార్ట్", "மெர்ஜ் சார்ட்", "ಮರ್ಜ್ ಸಾರ್ಟ್", "മെർജ് സോർട്ട്"],
        "answers": {
            "hinglish": (
                "Pattern hai divide and conquer with merge. Array ko aadha aadha baant-te jao jab tak har hissa ek element ka na ho jaye, phir sorted order mein wapas jodo. "
                "Merge step mein do sorted halves ko compare karke ek sorted list banate hain. Divide karna aasan hai, merge karna asli kaam hai. "
                "Time hamesha O of n log n hota hai, best worst average sab mein. Space hai O of n merge ke liye extra array ke kaaran. "
                "Trade-off: quick sort se predictable hai aur stable hai, lekin extra memory leta hai aur practice mein thoda slow ho sakta hai. Linked list par merge sort khaas taur par achha hai, kyunki wahan merge O of 1 space mein hota hai."
            ),
            "english": (
                "The pattern is divide and conquer with merging. Keep splitting the array in half until each piece has one element, then merge the pieces back in sorted order. "
                "The merge step compares two sorted halves to build one sorted list. Splitting is easy; merging is the real work. "
                "Time is always O of n log n, in the best, worst, and average cases. Space is O of n for the extra merge array. "
                "The trade-off: it is predictable and stable, unlike quick sort, but it uses extra memory and can be slower in practice. On linked lists it shines, because merging there takes O of 1 extra space."
            ),
            "telugu": (
                "Pattern: merge తో divide and conquer. Array ని సగం సగం విభజిస్తూ వెళ్లి, తర్వాత sorted order లో తిరిగి కలపండి. "
                "Merge step లో రెండు sorted halves ని compare చేసి ఒక sorted list తయారుచేస్తారు. Time ఎప్పుడూ O(n log n), space O(n). Stable, కానీ extra memory పడుతుంది."
            ),
            "tamil": (
                "Pattern: merge உடன் divide and conquer. Array-ஐ பாதி பாதியாகப் பிரித்து, பிறகு sorted order-ல் மீண்டும் இணைக்கவும். "
                "Merge step-ல் இரண்டு sorted halves-ஐ compare செய்து ஒரு sorted list உருவாக்குகிறோம். Time எப்போதும் O(n log n), space O(n). Stable, ஆனால் extra memory ஆகும்."
            ),
            "kannada": (
                "Pattern: merge ಜೊತೆ divide and conquer. Array ಅನ್ನು ಅರ್ಧ ಅರ್ಧ ವಿಭಜಿಸುತ್ತಾ ಹೋಗಿ, ನಂತರ sorted order ನಲ್ಲಿ ಮತ್ತೆ ಸೇರಿಸಿ. "
                "Merge step ನಲ್ಲಿ ಎರಡು sorted halves ಅನ್ನು compare ಮಾಡಿ ಒಂದು sorted list ಮಾಡುತ್ತಾರೆ. Time ಯಾವಾಗಲೂ O(n log n), space O(n). Stable, ಆದರೆ extra memory ಬೇಕು."
            ),
            "malayalam": (
                "Pattern: merge-ഓടെ divide and conquer. Array പകുതി പകുതിയായി വിഭജിച്ച്, പിന്നീട് sorted order-ൽ വീണ്ടും ചേർക്കുക. "
                "Merge step-ൽ രണ്ട് sorted halves compare ചെയ്ത് ഒരു sorted list ഉണ്ടാക്കുന്നു. Time എപ്പോഴും O(n log n), space O(n). Stable, പക്ഷേ extra memory വേണം."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: baanto, baanto, phir sorted order mein jodo. Jodna hi asli kaam hai.",
            "english": "Simply: split, split, then join back in sorted order. The joining is the real work.",
        },
        "example": "Example: [38,27,43,3] -> split to [38],[27],[43],[3] -> merge to [27,38],[3,43] -> [3,27,38,43].",
    },
    {
        "topic": "Kth Largest Element",
        "category": "Heap",
        "difficulty": "Medium",
        "keywords": ["kth largest", "kth largest element", "k largest", "kth smallest", "kth largest element in array", "find kth largest"],
        "answers": {
            "hinglish": (
                "Pattern hai min-heap of size k. Heap mein pehle k elements daalo, phir baaki har element ke liye dekho: agar element heap ke top se bada hai toh top hatao aur naya daalo. "
                "Aakhir mein heap ka top hi kth largest hota hai, kyunki heap mein sirf sabse bade k elements bache hote hain. "
                "Time hai O of n log k, space O of k. Trade-off: poora array sort karna O of n log n leta hai, heap wala tareeka behtar hai jab k chhota ho. "
                "Quickselect O of n average mein bhi kar sakta hai, lekin worst case aur samajhna mushkil hai. Heap wala solution interview mein safe aur saaf hai."
            ),
            "english": (
                "The pattern is a min-heap of size k. Put the first k elements in the heap, then for each remaining element: if it is larger than the heap top, remove the top and insert it. "
                "At the end, the heap top is the kth largest, because the heap holds only the k largest elements. "
                "Time is O of n log k, space O of k. The trade-off: sorting the whole array costs O of n log n; the heap method is better when k is small. "
                "Quickselect averages O of n but is harder to explain and has a bad worst case. The heap solution is the safe, clean interview answer."
            ),
            "telugu": (
                "Pattern: size k గల min-heap. మొదటి k elements heap లో వేసి, మిగిలిన ప్రతి element heap top కన్నా పెద్దదైతే top తీసేసి కొత్తది వేయండి. "
                "చివర్లో heap top ఏ kth largest. Time O(n log k), space O(k). Sort చేస్తే O(n log n) పడుతుంది; k చిన్నదైతే heap మంచిది."
            ),
            "tamil": (
                "Pattern: size k உள்ள min-heap. முதல் k elements-ஐ heap-ல் போட்டு, மீதமுள்ள ஒவ்வொரு element-ம் heap top-ஐ விட பெரியதாக இருந்தால் top-ஐ நீக்கி புதியதை போடுங்கள். "
                "முடிவில் heap top தான் kth largest. Time O(n log k), space O(k). Sort செய்தால் O(n log n) ஆகும்; k சிறியதாக இருந்தால் heap நல்லது."
            ),
            "kannada": (
                "Pattern: size k ಇರುವ min-heap. ಮೊದಲ k elements ಅನ್ನು heap ನಲ್ಲಿ ಹಾಕಿ, ಉಳಿದ ಪ್ರತಿ element heap top ಗಿಂತ ದೊಡ್ಡದಾಗಿದ್ದರೆ top ತೆಗೆದು ಹೊಸದನ್ನು ಹಾಕಿ. "
                "ಕೊನೆಯಲ್ಲಿ heap top ಏ kth largest. Time O(n log k), space O(k). Sort ಮಾಡಿದರೆ O(n log n) ಆಗುತ್ತದೆ; k ಚಿಕ್ಕದಾಗಿದ್ದರೆ heap ಒಳ್ಳೆಯದು."
            ),
            "malayalam": (
                "Pattern: size k ഉള്ള min-heap. ആദ്യ k elements heap-ൽ ഇട്ട്, ബാക്കി ഓരോ element-ഉം heap top-നേക്കാൾ വലുതാണെങ്കിൽ top നീക്കി പുതിയത് ഇടുക. "
                "അവസാനം heap top ആണ് kth largest. Time O(n log k), space O(k). Sort ചെയ്താൽ O(n log n) ആകും; k ചെറുതാണെങ്കിൽ heap നല്ലതാണ്."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: sirf sabse bade k numbers ka dabba rakho. Dabbe mein sabse chhota wala hi kth largest hai.",
            "english": "Simply: keep a box of only the k biggest numbers. The smallest number in the box is the kth largest.",
        },
        "example": "Example: nums = [3,2,1,5,6,4], k = 2 -> 5.",
    },
    {
        "topic": "Top K Frequent Elements",
        "category": "Heap",
        "difficulty": "Medium",
        "keywords": ["top k frequent", "top k frequent elements", "most frequent", "k frequent", "frequent elements", "top frequent"],
        "answers": {
            "hinglish": (
                "Pattern hai hash map plus heap, ya bucket sort. Pehle har element ki frequency gino hash map se. Phir do tareeke hain. "
                "Heap wala: frequency ke hisaab se min-heap mein top k rakho, time O of n log k. Bucket wala: frequency ko index banao, har frequency ke liye list rakho, phir peeche se k elements uthao, time O of n. "
                "Trade-off: bucket sort tez hai lekin O of n extra space leta hai aur samjhana thoda mushkil hai. Heap wala likhna aasan hai aur aksar acceptable hai. "
                "Interview mein pehle heap wala bolo, phir bucket wala optimisation ke roop mein batao."
            ),
            "english": (
                "The pattern is a hash map plus a heap, or bucket sort. First count each element's frequency with a hash map. Then two options. "
                "Heap: keep the top k by frequency in a min-heap, time O of n log k. Bucket: index lists by frequency, then collect k elements from the back, time O of n. "
                "The trade-off: bucket sort is faster but takes O of n extra space and is trickier to explain. The heap version is easier to write and usually acceptable. "
                "In an interview, state the heap version first, then offer bucket sort as the optimisation."
            ),
            "telugu": (
                "Pattern: hash map + heap, లేదా bucket sort. ముందు ప్రతి element frequency లెక్కించండి. Heap తో top k ఉంచితే O(n log k); "
                "bucket sort తో O(n). Bucket వేగంగా ఉంటుంది, కానీ O(n) space పడుతుంది. Interview లో ముందు heap చెప్పి, తర్వాత bucket optimisation గా చెప్పండి."
            ),
            "tamil": (
                "Pattern: hash map + heap, அல்லது bucket sort. முதலில் ஒவ்வொரு element-ன் frequency-ஐ எண்ணுங்கள். Heap கொண்டு top k வைத்தால் O(n log k); "
                "bucket sort கொண்டு O(n). Bucket வேகமானது, ஆனால் O(n) space ஆகும். Interview-ல் முதலில் heap சொல்லி, பிறகு bucket optimisation ஆக சொல்லுங்கள்."
            ),
            "kannada": (
                "Pattern: hash map + heap, ಅಥವಾ bucket sort. ಮೊದಲು ಪ್ರತಿ element ನ frequency ಎಣಿಸಿ. Heap ಜೊತೆ top k ಇಟ್ಟರೆ O(n log k); "
                "bucket sort ಜೊತೆ O(n). Bucket ವೇಗವಾಗಿದೆ, ಆದರೆ O(n) space ಬೇಕು. Interview ನಲ್ಲಿ ಮೊದಲು heap ಹೇಳಿ, ನಂತರ bucket optimisation ಆಗಿ ಹೇಳಿ."
            ),
            "malayalam": (
                "Pattern: hash map + heap, അല്ലെങ്കിൽ bucket sort. ആദ്യം ഓരോ element-ന്റെ frequency എണ്ണുക. Heap കൊണ്ട് top k വച്ചാൽ O(n log k); "
                "bucket sort കൊണ്ട് O(n). Bucket വേഗമാണ്, പക്ഷേ O(n) space വേണം. Interview-ൽ ആദ്യം heap പറഞ്ഞ്, പിന്നീട് bucket optimisation ആയി പറയുക."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: pehle gino kaun kitni baar aaya, phir sabse zyada baar aane wale k ko uthao.",
            "english": "Simply: count how often each value appears, then pick the k most common ones.",
        },
        "example": "Example: nums = [1,1,1,2,2,3], k = 2 -> [1,2].",
    },
]
