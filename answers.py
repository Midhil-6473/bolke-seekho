"""Bolke Seekho answer bank — multilingual.

Questions can be ASKED in 10 Indian languages (Prisma speech-to-text):
Hinglish, English, Telugu, Tamil, Kannada, Malayalam, Marathi, Bengali,
Gujarati, Punjabi. Tech terms (two sum, hash map, array) are spoken in
English in every language, so keyword matching works across all of them,
including native-script transcripts.

Full written answer banks exist for: hinglish, english, telugu, tamil,
kannada, malayalam. For marathi/bengali/gujarati/punjabi the question is
understood and the answer is spoken in English for now.

Every answer follows the AI-era style: pattern -> why it works ->
complexity -> trade-off / interview tip.
"""

# language key -> BCP-47 code used for Prisma STT
LANGUAGES = {
    "hinglish": "hi-IN",
    "english": "en-IN",
    "telugu": "te-IN",
    "tamil": "ta-IN",
    "kannada": "kn-IN",
    "malayalam": "ml-IN",
    "marathi": "mr-IN",
    "bengali": "bn-IN",
    "gujarati": "gu-IN",
    "punjabi": "pa-IN",
}

ANSWER_LANGS = ["hinglish", "english", "telugu", "tamil", "kannada", "malayalam"]


def answer_lang_for(lang: str) -> str:
    """Bank language to use for a UI language (falls back to english)."""
    return lang if lang in ANSWER_LANGS else "english"


ANSWERS = [
    {
        "topic": "Two Sum",
        "keywords": ["two sum", "2 sum", "to sum", "do sum", "टू सम", "do number ka sum", "pair sum", "target sum",
                      "టూ సమ్", "டூ சம்", "ಟೂ ಸಮ್", "ടൂ സം"],
        "answers": {
            "hinglish": (
                "Pattern hai hash map. Array ko ek baar scan karo, aur har number ke liye check karo "
                "ki uska partner, matlab target minus current number, pehle aa chuka hai ya nahi. "
                "Mila toh dono index mil gaye. Ye kaam isliye karta hai kyunki hum purane numbers ko "
                "yaad rakhte hain, dobara dhoondhne ki zaroorat nahi padti. Time hai O of n, space bhi O of n. "
                "Trade-off ye hai: brute force O of n square hota hai, yahan hum thodi memory deke speed lete hain. "
                "Interview mein ye trade-off bolna important hai."
            ),
            "english": (
                "The pattern is a hash map. Scan the array once, and for each number check whether its "
                "partner — target minus the current number — has already been seen. If yes, you have both "
                "indices. It works because you remember past numbers instead of searching for them again. "
                "Time is O of n, space is O of n. The trade-off: brute force takes O of n square; here you "
                "spend a little memory to buy speed, and you should say that trade-off out loud in the interview."
            ),
            "telugu": (
                "Pattern: hash map. Array ని ఒక్కసారి scan చేయండి. ప్రతి number కి, target minus ఆ number — "
                "ఆ partner ముందు వచ్చిందా అని check చేయండి. వస్తే రెండు indices దొరికాయి. ఎందుకంటే పాత numbers ని "
                "గుర్తు పెట్టుకుంటాం, మళ్ళీ వెతకాల్సిన అవసరం లేదు. Time complexity O(n), space O(n). "
                "Brute force O(n square) కన్నా ఇది fast; కొంచెం memory ఎక్కువ వాడతాం — interview లో ఈ trade-off చెప్పాలి."
            ),
            "tamil": (
                "Pattern: hash map. Array-ஐ ஒரு முறை scan செய்யுங்கள். ஒவ்வொரு number-க்கும், target minus அந்த number — "
                "அந்த partner முன்பு வந்ததா என்று check செய்யுங்கள். வந்திருந்தால் இரண்டு indices கிடைத்துவிடும். "
                "பழைய numbers-ஐ நினைவில் வைப்பதால் இது வேலை செய்கிறது. Time complexity O(n), space O(n). "
                "Brute force O(n square)-ஐ விட இது fast; கொஞ்சம் memory அதிகம் — interview-ல் இந்த trade-off சொல்ல வேண்டும்."
            ),
            "kannada": (
                "Pattern: hash map. Array ಅನ್ನು ಒಂದು ಬಾರಿ scan ಮಾಡಿ. ಪ್ರತಿ number ಗೆ, target minus ಆ number — "
                "ಆ partner ಮೊದಲು ಬಂದಿದೆಯೇ ಎಂದು check ಮಾಡಿ. ಬಂದಿದ್ದರೆ ಎರಡು indices ಸಿಕ್ಕಿತು. ಹಳೆಯ numbers ಅನ್ನು "
                "ನೆನಪಿಡುವುದರಿಂದ ಇದು ಕೆಲಸ ಮಾಡುತ್ತದೆ. Time complexity O(n), space O(n). Brute force O(n square) ಕ್ಕಿಂತ "
                "ಇದು fast; ಸ್ವಲ್ಪ memory ಹೆಚ್ಚು — interview ನಲ್ಲಿ ಈ trade-off ಹೇಳಬೇಕು."
            ),
            "malayalam": (
                "Pattern: hash map. Array ഒരിക്കൽ scan ചെയ്യുക. ഓരോ number-നും, target minus ആ number — "
                "ആ partner നേരത്തെ വന്നിട്ടുണ്ടോ എന്ന് check ചെയ്യുക. ഉണ്ടെങ്കിൽ രണ്ട് indices കിട്ടി. പഴയ numbers "
                "ഓർത്തുവെക്കുന്നതുകൊണ്ടാണ് ഇത് work ചെയ്യുന്നത്. Time complexity O(n), space O(n). "
                "Brute force O(n square)-നേക്കാൾ ഇത് fast ആണ്; കുറച്ച് memory കൂടുതൽ — interview-ൽ ഈ trade-off പറയണം."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: har number ke saath uska partner dhoondho. Partner pehle mila hai toh jawab mil gaya. Partner ko yaad rakhne ke liye hash map use hota hai.",
            "english": "Simply: for every number, look for its partner that completes the target. A hash map remembers the numbers you have already seen, so each lookup is instant.",
        },
        "example": "Example: array hai 2, 7, 11, 15 aur target 9. 2 ke liye partner 7 chahiye, abhi nahi mila. Phir 7 aaya, uska partner 2 pehle se map mein hai. Answer: index 0 aur 1.",
    },
    {
        "topic": "3Sum",
        "keywords": ["3sum", "3 sum", "three sum", "थ्री सम", "teen number", "triplet",
                      "త్రీ సమ్", "த்ரீ சம்", "ತ್ರೀ ಸಮ್", "ത്രീ സം"],
        "answers": {
            "hinglish": (
                "Pattern hai sort karke two pointers. Pehle array sort karo, phir ek number fix karo, "
                "aur baaki do ko left aur right pointer se dhoondho. Sum chhota hai toh left badhao, "
                "bada hai toh right ghatao. Sorting ki wajah se pointers ek hi direction mein chalte hain, "
                "isliye har fixed number ke liye linear scan kaafi hai. Time hai O of n square, space O of 1 extra. "
                "Trade-off: duplicates skip karna bhoolna sabse common galti hai, aur bina sort kiye two pointer chalega hi nahi."
            ),
            "english": (
                "The pattern is sort plus two pointers. Sort the array, fix one number, then hunt the other "
                "two with a left and a right pointer. Sum too small, move left up; too big, move right down. "
                "Sorting lets both pointers move in one direction only, so each fixed number costs a linear scan. "
                "Time is O of n square, extra space O of 1. The common trap is forgetting to skip duplicates — "
                "and two pointers simply do not work on an unsorted array."
            ),
            "telugu": (
                "Pattern: ముందు array sort చేయండి, తర్వాత two pointers. ఒక number fix చేసి, మిగilin రెండు numbers ని "
                "left, right pointers తో వెతకండి. Sum చిన్నదైతే left పెంచండి, పెద్దదైతే right తగ్గించండి. "
                "Time complexity O(n square). Duplicates skip చేయడం మర్చిపోవడం common mistake."
            ),
            "tamil": (
                "Pattern: முதலில் array-ஐ sort செய்யுங்கள், பிறகு two pointers. ஒரு number-ஐ fix செய்து, மீதமுள்ள "
                "இரண்டையும் left, right pointers கொண்டு தேடுங்கள். Sum சிறியதாக இருந்தால் left-ஐ நகர்த்தவும், "
                "பெரியதாக இருந்தால் right-ஐ நகர்த்தவும். Time complexity O(n square). Duplicates-ஐ skip செய்ய மறப்பது common mistake."
            ),
            "kannada": (
                "Pattern: ಮೊದಲು array ಅನ್ನು sort ಮಾಡಿ, ನಂತರ two pointers. ಒಂದು number ಅನ್ನು fix ಮಾಡಿ, ಉಳಿದ ಎರಡನ್ನು "
                "left, right pointers ನಿಂದ ಹುಡುಕಿ. Sum ಚಿಕ್ಕದಾದರೆ left ಹೆಚ್ಚಿಸಿ, ದೊಡ್ಡದಾದರೆ right ಕಡಿಮೆ ಮಾಡಿ. "
                "Time complexity O(n square). Duplicates skip ಮಾಡಲು ಮರೆಯುವುದು common mistake."
            ),
            "malayalam": (
                "Pattern: ആദ്യം array sort ചെയ്യുക, പിന്നെ two pointers. ഒരു number fix ചെയ്ത്, ബാക്കി രണ്ടിനെ "
                "left, right pointers വെച്ച് തിരയുക. Sum ചെറുതാണെങ്കിൽ left കൂട്ടുക, വലുതാണെങ്കിൽ right കുറയ്ക്കുക. "
                "Time complexity O(n square). Duplicates skip ചെയ്യാൻ മറക്കുന്നത് common mistake ആണ്."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: array sort karo, ek number pakdo, aur baaki do ko dono ends se beech ki taraf laakar dhoondho.",
            "english": "Simply: sort the array, hold one number fixed, and close in on the other two from both ends.",
        },
        "example": "Example: array hai minus 1, 0, 1, 2, minus 1, minus 4. Sorted karke fix karo minus 1, pointers se 1 aur 0 milte hain — triplet: minus 1, 0, 1, sum zero.",
    },
    {
        "topic": "Container With Most Water",
        "keywords": ["container", "most water", "पानी", "paani", "max water", "max area",
                      "കണ്ടെയ്നർ", "கன்டெய்னர்", "కంటైనర్", "ಕಂಟೈನರ್"],
        "answers": {
            "hinglish": (
                "Pattern hai two pointers, dono ends se. Area hota hai chhoti height guna width. "
                "Har step par chhoti wali side ko andar move karo, kyunki badi side ko move karne se "
                "area kabhi badh nahi sakta, width toh ghat hi rahi hai. Ye greedy move isliye sahi hai "
                "kyunki chhoti height hi area ki limit hai. Time hai O of n, space O of 1. "
                "Trade-off: ye sirf tab kaam karta hai jab do ends ke beech ka area chahiye, har pair check karne ki zaroorat nahi."
            ),
            "english": (
                "The pattern is two pointers from both ends. Area is the shorter height times the width. "
                "Each step, move the shorter side inward: moving the taller side can never help, because "
                "the width only shrinks and the short side caps the area anyway. Time is O of n, space O of 1. "
                "The trade-off: this greedy shortcut only works because the area is defined by the two ends — "
                "you never need to check every pair."
            ),
            "telugu": (
                "Pattern: two pointers, రెండు చివర్ల నుంచి. Area అంటే చిన్న height into width. ప్రతి step లో "
                "చిన్న side ని లోపలికి move చేయండి — పెద్ద side move చేస్తే area పెరగదు, ఎందుకంటే width తగ్గుతుంది. "
                "Time complexity O(n), space O(1)."
            ),
            "tamil": (
                "Pattern: two pointers, இரண்டு முனைகளிலிருந்தும். Area என்பது சிறிய height பெருக்கல் width. "
                "ஒவ்வொரு step-லும் சிறிய side-ஐ உள்ளே நகர்த்துங்கள் — பெரிய side-ஐ நகர்த்தினால் area கூடாது, "
                "width குறைந்து கொண்டே போகும். Time complexity O(n), space O(1)."
            ),
            "kannada": (
                "Pattern: two pointers, ಎರಡು ತುದಿಗಳಿಂದ. Area ಎಂದರೆ ಚಿಕ್ಕ height ಗುಣಿಸಿದ width. ಪ್ರತಿ step ನಲ್ಲಿ "
                "ಚಿಕ್ಕ side ಅನ್ನು ಒಳಗೆ move ಮಾಡಿ — ದೊಡ್ಡ side move ಮಾಡಿದರೆ area ಹೆಚ್ಚಾಗುವುದಿಲ್ಲ, width ಕಡಿಮೆಯಾಗುತ್ತಲೇ ಇರುತ್ತದೆ. "
                "Time complexity O(n), space O(1)."
            ),
            "malayalam": (
                "Pattern: two pointers, രണ്ട് അറ്റത്തുനിന്നും. Area എന്നാൽ ചെറിയ height ഗുണം width. ഓരോ step-ലും "
                "ചെറിയ side അകത്തേക്ക് move ചെയ്യുക — വലിയ side move ചെയ്താൽ area കൂടില്ല, width കുറഞ്ഞുകൊണ്ടിരിക്കും. "
                "Time complexity O(n), space O(1)."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: dono kinare se shuru karo, jo side chhoti hai use andar lao. Chhoti side hi paani ki limit hai.",
            "english": "Simply: start from both edges and keep moving the shorter wall inward — the short wall is what limits the water.",
        },
        "example": "Example: heights hai 1, 8, 6, 2, 5, 4, 8, 3, 7. Ends par 1 aur 7: area 7. Chhoti side 1 ko hatao, phir 8 aur 7 milte hain: area 49. Yahi maximum hai.",
    },
    {
        "topic": "Best Time to Buy and Sell Stock",
        "keywords": ["stock", "स्टॉक", "share", "शेयर", "kharid", "bech", "profit", "buy and sell",
                      "షేర్", "ஷேர்", "ಶೇರ್", "ഷെയർ", "స్టాక్", "ஸ்டாக்", "ಸ್ಟಾಕ್", "സ്റ്റോക്ക്"],
        "answers": {
            "hinglish": (
                "Pattern hai ek hi scan mein minimum price yaad rakhna. Jaise jaise aage badho, "
                "ab tak ka sabse sasta price maintain karo, aur har din check karo ki aaj bechne par "
                "kitna profit hoga. Ye isliye kaam karta hai kyunki best deal hamesha kisi purane minimum "
                "ke against hi banti hai. Time hai O of n, space O of 1. "
                "Trade-off: ye sirf ek transaction ke liye hai. Do transactions ya fee wala version aaye toh DP lagega."
            ),
            "english": (
                "The pattern is one scan while remembering the minimum price so far. Keep updating the "
                "cheapest price seen, and at each day ask: if I sold today, what is my profit? It works "
                "because the best deal is always measured against some earlier minimum. Time is O of n, "
                "space O of 1. The trade-off: this solves a single transaction; two transactions or a fee "
                "turns it into a DP problem."
            ),
            "telugu": (
                "Pattern: ఒకే scan లో minimum price గుర్తుంచుకోవడం. ఇప్పటివరకు చూసిన అత్యంత చౌక price ని maintain చేయండి, "
                "ప్రతి రోజు — ఈ రోజు అమ్మితే ఎంత profit? అని check చేయండి. Time complexity O(n), space O(1). "
                "ఇది ఒకే transaction కోసం; రెండు transactions అంటే DP వాడాలి."
            ),
            "tamil": (
                "Pattern: ஒரே scan-ல் minimum price-ஐ நினைவில் வைப்பது. இதுவரை பார்த்த மிகக் குறைந்த price-ஐ maintain "
                "செய்யுங்கள், ஒவ்வொரு நாளும் — இன்று விற்றால் எவ்வளவு profit? என்று check செய்யுங்கள். "
                "Time complexity O(n), space O(1). இது ஒரே transaction-க்கு; இரண்டு transactions என்றால் DP வேண்டும்."
            ),
            "kannada": (
                "Pattern: ಒಂದೇ scan ನಲ್ಲಿ minimum price ಅನ್ನು ನೆನಪಿಡುವುದು. ಇದುವರೆಗೆ ನೋಡಿದ ಅತ್ಯಂತ ಅಗ್ಗದ price ಅನ್ನು maintain "
                "ಮಾಡಿ, ಪ್ರತಿ ದಿನ — ಇಂದು ಮಾರಿದರೆ ಎಷ್ಟು profit? ಎಂದು check ಮಾಡಿ. Time complexity O(n), space O(1). "
                "ಇದು ಒಂದು transaction ಗೆ ಮಾತ್ರ; ಎರಡು transactions ಆದರೆ DP ಬೇಕು."
            ),
            "malayalam": (
                "Pattern: ഒരൊറ്റ scan-ൽ minimum price ഓർത്തുവെക്കുക. ഇതുവരെ കണ്ട ഏറ്റവും കുറഞ്ഞ price maintain ചെയ്യുക, "
                "ഓരോ ദിവസവും — ഇന്ന് വിറ്റാൽ എത്ര profit? എന്ന് check ചെയ്യുക. Time complexity O(n), space O(1). "
                "ഇത് ഒരു transaction-ന് മാത്രം; രണ്ട് transactions ആണെങ്കിൽ DP വേണം."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: sabse sasta din yaad rakho, aur har din usi se bechne ka profit check karo. Sabse bada profit hi jawab hai.",
            "english": "Simply: remember the cheapest day so far, and check the selling profit against it every day. The biggest profit wins.",
        },
        "example": "Example: prices hai 7, 1, 5, 3, 6, 4. Sabse sasta 1 hai. Uske baad 6 par becho toh profit 5. Yahi maximum hai.",
    },
    {
        "topic": "Product of Array Except Self",
        "keywords": ["product except self", "except self", "guna", "गुणा", "product of array",
                      "ప్రోడక్ట్", "ப்ராடக்ட்", "ಪ್ರಾಡಕ್ಟ್", "പ്രോഡക്റ്റ്"],
        "answers": {
            "hinglish": (
                "Pattern hai prefix aur suffix product. Har index ke liye left side ka total product "
                "aur right side ka total product alag se rakho, phir answer hai dono ka guna. "
                "Division bilkul use nahi karna, kyunki zero aate hi division fail ho jayega. "
                "Pehle left products result array mein bharo, phir right se ulta scan karke multiply kar do. "
                "Time hai O of n, aur extra space O of 1 kyunki result array count nahi hota. "
                "Trade-off: do pass lagte hain, lekin division wale shortcut se zyada safe hai."
            ),
            "english": (
                "The pattern is prefix and suffix products. For each index you need the product of "
                "everything on its left times everything on its right. Never use division — a single zero "
                "breaks it. Fill the result with left products in one pass, then scan from the right "
                "multiplying in the right products. Time is O of n, extra space O of 1 since the result "
                "array does not count. The trade-off: two passes, but far safer than the division shortcut."
            ),
            "telugu": (
                "Pattern: prefix మరియు suffix products. ప్రతి index కి, ఎడమ వైపు మొత్తం product మరియు కుడి వైపు మొత్తం "
                "product కలపండి. Division అస్సలు వాడొద్దు — zero వస్తే fail అవుతుంది. Time complexity O(n), extra space O(1)."
            ),
            "tamil": (
                "Pattern: prefix மற்றும் suffix products. ஒவ்வொரு index-க்கும், இடது பக்க மொத்த product மற்றும் வலது பக்க "
                "மொத்த product-ஐ பெருக்குங்கள். Division பயன்படுத்தவே கூடாது — zero வந்தால் fail ஆகும். "
                "Time complexity O(n), extra space O(1)."
            ),
            "kannada": (
                "Pattern: prefix ಮತ್ತು suffix products. ಪ್ರತಿ index ಗೆ, ಎಡಭಾಗದ ಒಟ್ಟು product ಮತ್ತು ಬಲಭಾಗದ ಒಟ್ಟು product "
                "ಅನ್ನು ಗುಣಿಸಿ. Division ಬಳಸಲೇಬೇಡಿ — zero ಬಂದರೆ fail ಆಗುತ್ತದೆ. Time complexity O(n), extra space O(1)."
            ),
            "malayalam": (
                "Pattern: prefix-ഉം suffix products-ഉം. ഓരോ index-നും, ഇടതുവശത്തെ ആകെ product-ഉം വലതുവശത്തെ ആകെ "
                "product-ഉം ഗുണിക്കുക. Division ഉപയോഗിക്കരുത് — zero വന്നാൽ fail ആകും. Time complexity O(n), extra space O(1)."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: har number ke liye baayein ka guna aur daayein ka guna multiply kar do. Division kabhi nahi.",
            "english": "Simply: for each position, multiply the product of everything on its left by the product of everything on its right. No division, ever.",
        },
        "example": "Example: array hai 1, 2, 3, 4. Index 1 par value 2 hai: left product 1, right product 3 guna 4 matlab 12. Answer wahan 12. Poora answer: 24, 12, 8, 6.",
    },
    {
        "topic": "Longest Consecutive Sequence",
        "keywords": ["consecutive", "lagatar", "लगातार", "sequence", "longest consecutive"],
        "answers": {
            "hinglish": (
                "Pattern hai hash set. Saare numbers set mein daal do. Phir sirf un numbers se sequence "
                "shuru karo jinka pichla number set mein nahi hai, matlab jo sequence ka start ho sakte hain. "
                "Wahan se aage count karo. Har number sirf ek baar sequence ke andar visit hota hai, isliye "
                "total time O of n hai, sorting wale O of n log n se better. Space hai O of n set ke liye. "
                "Trade-off: memory zyada lagti hai, lekin interview mein O of n solution hi expected hota hai."
            ),
            "english": (
                "The pattern is a hash set. Put all numbers in a set, then only start counting a sequence "
                "from a number whose predecessor is not in the set — a true sequence start. Each number is "
                "visited once inside a sequence, so total time is O of n, beating the O of n log n sort. "
                "Space is O of n for the set. The trade-off: more memory, but O of n is what the interview expects."
            ),
            "telugu": (
                "Pattern: hash set. అన్ని numbers ని set లో వేయండి. తర్వాత, ముందు number set లో లేని numbers నుంచి మాత్రమే "
                "sequence ప్రారంభించండి — అవే నిజమైన starts. ప్రతి number ఒక్కసారే visit అవుతుంది కాబట్టి time O(n). Space O(n)."
            ),
            "tamil": (
                "Pattern: hash set. எல்லா numbers-ஐயும் set-ல் போடுங்கள். பிறகு, முந்தைய number set-ல் இல்லாத "
                "numbers-லிருந்து மட்டுமே sequence தொடங்குங்கள் — அவைதான் உண்மையான starts. ஒவ்வொரு number-ம் "
                "ஒருமுறை மட்டுமே visit ஆவதால் time O(n). Space O(n)."
            ),
            "kannada": (
                "Pattern: hash set. ಎಲ್ಲಾ numbers ಅನ್ನು set ನಲ್ಲಿ ಹಾಕಿ. ನಂತರ, ಹಿಂದಿನ number set ನಲ್ಲಿ ಇಲ್ಲದ numbers "
                "ನಿಂದ ಮಾತ್ರ sequence ಆರಂಭಿಸಿ — ಅವೇ ನಿಜವಾದ starts. ಪ್ರತಿಯೊಂದು number ಒಮ್ಮೆ ಮಾತ್ರ visit ಆಗುವುದರಿಂದ time O(n). Space O(n)."
            ),
            "malayalam": (
                "Pattern: hash set. എല്ലാ numbers-ഉം set-ൽ ഇടുക. പിന്നെ, മുൻപത്തെ number set-ൽ ഇല്ലാത്ത numbers-ൽ "
                "നിന്ന് മാത്രം sequence തുടങ്ങുക — അവയാണ് യഥാർത്ഥ starts. ഓരോ number-ഉം ഒരിക്കൽ മാത്രം visit ചെയ്യുന്നതുകൊണ്ട് time O(n). Space O(n)."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: saare numbers ko set mein rakho, aur sirf wahan se ginti shuru karo jahan se nayi chain banti hai.",
            "english": "Simply: keep all numbers in a set, and only start counting where a new chain begins.",
        },
        "example": "Example: numbers hai 100, 4, 200, 1, 3, 2. Chain 1, 2, 3, 4 banti hai — length 4. Yahi longest hai.",
    },
]

ANSWERS += [
    {
        "topic": "Subarray Sum Equals K (Prefix Sum)",
        "keywords": ["prefix sum", "subarray sum", "subarray", "सबएरे", "sum equals k", "sum barabar k",
                      "సబ్అరే", "சப்அரே", "ಸಬ್ಅರೇ", "സബ്അറേ"],
        "answers": {
            "hinglish": (
                "Pattern hai prefix sum ke saath hash map. Chalte chalte cumulative sum rakho. "
                "Agar current prefix sum minus k pehle kahin aa chuka hai, toh beech wala subarray ka sum exactly k hai. "
                "Map mein har prefix sum kitni baar aaya, ye count rakho, aur zero prefix sum ko count ek se shuru karo. "
                "Time hai O of n, space O of n. Trade-off: negative numbers hon toh sliding window fail ho jata hai, "
                "isiliye yahan hash map wala tareeka hi sahi hai."
            ),
            "english": (
                "The pattern is prefix sum with a hash map. Keep a running cumulative sum. If the current "
                "prefix sum minus k has appeared before, the subarray between those points sums to exactly k. "
                "Store how many times each prefix sum occurred, starting with zero seen once. Time is O of n, "
                "space O of n. The trade-off: with negative numbers, sliding window breaks — the hash map is "
                "the right tool here."
            ),
            "telugu": (
                "Pattern: prefix sum మరియు hash map. నడుస్తూ cumulative sum ఉంచండి. Current prefix sum minus k "
                "ముందు వచ్చి ఉంటే, మధ్యలో ఉన్న subarray sum exactly k. Time complexity O(n), space O(n). "
                "Negative numbers ఉంటే sliding window పనిచేయదు — అందుకే hash map వాడాలి."
            ),
            "tamil": (
                "Pattern: prefix sum உடன் hash map. ஓடிக்கொண்டே cumulative sum வைத்திருங்கள். Current prefix sum minus k "
                "முன்பு வந்திருந்தால், நடுவில் உள்ள subarray sum சரியாக k. Time complexity O(n), space O(n). "
                "Negative numbers இருந்தால் sliding window வேலை செய்யாது — அதனால் hash map தான் சரி."
            ),
            "kannada": (
                "Pattern: prefix sum ಜೊತೆಗೆ hash map. ಓಡುತ್ತಾ cumulative sum ಇಟ್ಟುಕೊಳ್ಳಿ. Current prefix sum minus k "
                "ಮೊದಲು ಬಂದಿದ್ದರೆ, ಮಧ್ಯದ subarray sum ನಿಖರವಾಗಿ k. Time complexity O(n), space O(n). "
                "Negative numbers ಇದ್ದರೆ sliding window ಕೆಲಸ ಮಾಡುವುದಿಲ್ಲ — ಹಾಗಾಗಿ hash map ಸರಿ."
            ),
            "malayalam": (
                "Pattern: prefix sum-ഉം hash map-ഉം. ഓടിക്കൊണ്ട് cumulative sum സൂക്ഷിക്കുക. Current prefix sum minus k "
                "നേരത്തെ വന്നിട്ടുണ്ടെങ്കിൽ, ഇടയിലുള്ള subarray sum കൃത്യമായി k. Time complexity O(n), space O(n). "
                "Negative numbers ഉണ്ടെങ്കിൽ sliding window work ചെയ്യില്ല — അതുകൊണ്ട് hash map ആണ് ശരി."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: chalta hua total rakho. Agar total minus k pehle dikha tha, toh beech ka hissa hi jawab hai.",
            "english": "Simply: keep a running total. If total minus k was seen before, the stretch in between is your answer.",
        },
        "example": "Example: array hai 1, 1, 1 aur k hai 2. Prefix sums: 0, 1, 2, 3. Prefix 0 ke baad 2 aaya — ek subarray. Phir 1 ke baad 3 — dusra. Total 2 subarrays.",
    },
    {
        "topic": "Remove Duplicates from Sorted Array",
        "keywords": ["remove duplicate", "duplicate hatao", "डुप्लिकेट", "duplicates",
                      "డూప్లికేట్", "டூப்ளிகேட்", "ಡೂಪ್ಲಿಕೇಟ್", "ഡ്യൂപ്ലിക്കേറ്റ്"],
        "answers": {
            "hinglish": (
                "Pattern hai two pointers, ek read pointer aur ek write pointer. Array sorted hai, "
                "isliye duplicates hamesha saath saath aayenge. Read pointer sab ko scan karta hai, "
                "aur jab naya value mile tabhi write pointer aage badhta hai aur value wahan likhi jaati hai. "
                "Time hai O of n, space O of 1, aur koi extra array nahi banta. "
                "Trade-off: ye sirf sorted array par kaam karta hai, unsorted mein set ya map lagega."
            ),
            "english": (
                "The pattern is two pointers: a read pointer and a write pointer. Because the array is "
                "sorted, duplicates always sit together. The read pointer scans everything; the write "
                "pointer advances only when a new value appears, and writes it there. Time is O of n, "
                "space O of 1, no extra array. The trade-off: this only works when sorted — unsorted "
                "input needs a set or a map."
            ),
            "telugu": (
                "Pattern: two pointers — ఒక read pointer, ఒక write pointer. Array sorted కాబట్టి duplicates "
                "ఎప్పుడూ పక్కపక్కనే ఉంటాయి. కొత్త value వచ్చినప్పుడే write pointer ముందుకు వెళ్తుంది. "
                "Time complexity O(n), space O(1). ఇది sorted array పైన మాత్రమే పనిచేస్తుంది."
            ),
            "tamil": (
                "Pattern: two pointers — ஒரு read pointer, ஒரு write pointer. Array sorted என்பதால் duplicates "
                "எப்போதும் அருகருகே இருக்கும். புதிய value வரும்போது மட்டுமே write pointer முன்னேறும். "
                "Time complexity O(n), space O(1). இது sorted array-ல் மட்டுமே வேலை செய்யும்."
            ),
            "kannada": (
                "Pattern: two pointers — ಒಂದು read pointer, ಒಂದು write pointer. Array sorted ಆಗಿರುವುದರಿಂದ duplicates "
                "ಯಾವಾಗಲೂ ಪಕ್ಕಪಕ್ಕದಲ್ಲೇ ಇರುತ್ತವೆ. ಹೊಸ value ಬಂದಾಗ ಮಾತ್ರ write pointer ಮುಂದೆ ಹೋಗುತ್ತದೆ. "
                "Time complexity O(n), space O(1). ಇದು sorted array ನಲ್ಲಿ ಮಾತ್ರ ಕೆಲಸ ಮಾಡುತ್ತದೆ."
            ),
            "malayalam": (
                "Pattern: two pointers — ഒരു read pointer, ഒരു write pointer. Array sorted ആയതുകൊണ്ട് duplicates "
                "എപ്പോഴും അടുത്തടുത്ത് ഇരിക്കും. പുതിയ value വരുമ്പോൾ മാത്രമേ write pointer മുന്നോട്ട് പോകൂ. "
                "Time complexity O(n), space O(1). ഇത് sorted array-ൽ മാത്രമേ work ചെയ്യൂ."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: ek pointer padhta hai, dusra sirf naye numbers likhta hai. Duplicates apne aap peeche reh jaate hain.",
            "english": "Simply: one pointer reads everything, the other writes only new values. Duplicates get left behind automatically.",
        },
        "example": "Example: array hai 1, 1, 2, 2, 3. Read pointer chalta hai, write pointer sirf 1, 2, 3 likhta hai. Pehle 3 positions hi jawab hain.",
    },
    {
        "topic": "Move Zeroes",
        "keywords": ["move zero", "zeroes", "zero", "ज़ीरो", "शून्य", "end mein zero",
                      "జీరో", "ஜீரோ", "ಜೀರೋ", "സീറോ"],
        "answers": {
            "hinglish": (
                "Pattern hai two pointers, bilkul remove duplicates jaisa. Ek write pointer rakho. "
                "Jo number zero nahi hai, use write pointer wali jagah par le aao aur pointer badhao. "
                "Aakhir mein bachi hui jagah zero se bhar do. Order bhi maintain rehta hai aur extra space bhi nahi lagta. "
                "Time hai O of n, space O of 1. Trade-off: swaps zyada ho sakte hain, lekin in-place solution ke liye ye standard hai."
            ),
            "english": (
                "The pattern is two pointers, the same family as remove duplicates. Keep a write pointer. "
                "Whenever a non-zero number appears, move it to the write position and advance. At the end, "
                "fill the remaining spots with zeroes. Order is preserved and no extra space is used. "
                "Time is O of n, space O of 1. The trade-off: there can be many swaps, but this is the "
                "standard in-place solution."
            ),
            "telugu": (
                "Pattern: two pointers. ఒక write pointer ఉంచండి. Zero కాని number వచ్చినప్పుడల్లా దాన్ని write "
                "position కి తీసుకురండి. చివర్లో మిగిలిన చోట్ల zeroes నింపండి. Order maintain అవుతుంది, extra space లేదు. "
                "Time complexity O(n), space O(1)."
            ),
            "tamil": (
                "Pattern: two pointers. ஒரு write pointer வைத்திருங்கள். Zero அல்லாத number வரும்போதெல்லாம் அதை write "
                "position-க்கு கொண்டு வாருங்கள். கடைசியில் மீதமுள்ள இடங்களில் zeroes நிரப்புங்கள். Order maintain ஆகும், "
                "extra space இல்லை. Time complexity O(n), space O(1)."
            ),
            "kannada": (
                "Pattern: two pointers. ಒಂದು write pointer ಇಟ್ಟುಕೊಳ್ಳಿ. Zero ಅಲ್ಲದ number ಬಂದಾಗಲೆಲ್ಲಾ ಅದನ್ನು write "
                "position ಗೆ ತನ್ನಿ. ಕೊನೆಯಲ್ಲಿ ಉಳಿದ ಜಾಗಗಳಲ್ಲಿ zeroes ತುಂಬಿ. Order maintain ಆಗುತ್ತದೆ, extra space ಇಲ್ಲ. "
                "Time complexity O(n), space O(1)."
            ),
            "malayalam": (
                "Pattern: two pointers. ഒരു write pointer വെക്കുക. Zero അല്ലാത്ത number വരുമ്പോഴെല്ലാം അതിനെ write "
                "position-ലേക്ക് കൊണ്ടുവരിക. അവസാനം ബാക്കിയുള്ള സ്ഥലങ്ങളിൽ zeroes നിറയ്ക്കുക. Order maintain ചെയ്യും, "
                "extra space ഇല്ല. Time complexity O(n), space O(1)."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: zero wale numbers ko peeche dhakel do — pehle saare non-zero aage, phir saare zero peeche.",
            "english": "Simply: push all non-zero numbers to the front in order, then fill the back with zeroes.",
        },
        "example": "Example: array hai 0, 1, 0, 3, 12. Non-zero numbers aage: 1, 3, 12. Peeche zero bhar do: 1, 3, 12, 0, 0.",
    },
    {
        "topic": "Longest Substring Without Repeating Characters",
        "keywords": ["substring", "repeat", "bina repeat", "longest substring", "sliding window substring",
                      "సబ్‌స్ట్రింగ్", "சப்ஸ்ட்ரிங்", "ಸಬ್‌ಸ್ಟ್ರಿಂಗ್", "സബ്സ്ട്രിംഗ്"],
        "answers": {
            "hinglish": (
                "Pattern hai sliding window ke saath last index ka map. Right pointer window badhata hai. "
                "Jaise hi koi character repeat ho, left pointer ko us character ke pichle index se ek aage le jao. "
                "Window ke andar kabhi duplicate nahi rehta, isliye har window valid hoti hai aur sabse lambi hi answer hai. "
                "Time hai O of n, space characters ke set ke size ke barabar. "
                "Trade-off: left pointer kabhi peeche nahi jaata, yahi is pattern ki pehchan hai."
            ),
            "english": (
                "The pattern is a sliding window with a last-seen index map. The right pointer grows the "
                "window. The moment a character repeats, jump the left pointer to just after that "
                "character's previous position. The window never holds a duplicate, so every window is "
                "valid and the longest one is the answer. Time is O of n; space is the size of the "
                "character set. The key insight: the left pointer never moves backwards."
            ),
            "telugu": (
                "Pattern: sliding window మరియు last index map. Right pointer window ని పెంచుతుంది. ఏ character "
                "అయినా repeat అయితే, left pointer ని ఆ character మునుపటి position తర్వాతకి జరపండి. "
                "Window లో duplicate ఎప్పుడూ ఉండదు. Time complexity O(n)."
            ),
            "tamil": (
                "Pattern: sliding window உடன் last index map. Right pointer window-ஐ வளர்க்கும். ஏதாவது character "
                "repeat ஆனவுடன், left pointer-ஐ அந்த character-ன் முந்தைய position-க்கு அடுத்ததாக நகர்த்துங்கள். "
                "Window-க்குள் duplicate எப்போதும் இருக்காது. Time complexity O(n)."
            ),
            "kannada": (
                "Pattern: sliding window ಜೊತೆಗೆ last index map. Right pointer window ಅನ್ನು ಬೆಳೆಸುತ್ತದೆ. ಯಾವುದೇ character "
                "repeat ಆದ ಕೂಡಲೇ, left pointer ಅನ್ನು ಆ character ನ ಹಿಂದಿನ position ನ ನಂತರಕ್ಕೆ ಸರಿಸಿ. "
                "Window ನಲ್ಲಿ duplicate ಎಂದಿಗೂ ಇರುವುದಿಲ್ಲ. Time complexity O(n)."
            ),
            "malayalam": (
                "Pattern: sliding window-ഉം last index map-ഉം. Right pointer window വളർത്തും. ഏതെങ്കിലും character "
                "repeat ആയാൽ, left pointer-നെ ആ character-ന്റെ മുൻപത്തെ position-ന് ശേഷം നീക്കുക. "
                "Window-ൽ duplicate ഒരിക്കലും ഉണ്ടാകില്ല. Time complexity O(n)."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: ek khidki rakho jisme koi letter do baar na ho. Letter repeat ho toh khidki ko aage se chhota kar do.",
            "english": "Simply: keep a window with no repeated letter. When a letter repeats, shrink the window from the left.",
        },
        "example": "Example: string hai a b c a b c b b. Window a b c banti hai, phir a repeat hota hai toh window aage badhti hai. Sabse lambi window ki length 3 hai.",
    },
    {
        "topic": "Valid Anagram",
        "keywords": ["anagram", "एनाग्राम", "అనాగ్రామ్", "அனகிராம்", "ಅನಾಗ್ರಾಮ್", "അനഗ്രാം"],
        "answers": {
            "hinglish": (
                "Pattern hai frequency count. Pehli string ke har character ki count badhao, "
                "dusri string ke har character ki count ghatao. Aakhir mein saari counts zero honi chahiye. "
                "Chhote alphabet ke liye size 26 ka array kaafi hai, general case mein hash map use karo. "
                "Time hai O of n, space O of 1 array wale version mein. "
                "Trade-off: sorting wala solution O of n log n hai, frequency count usse tez aur simple hai."
            ),
            "english": (
                "The pattern is frequency counting. Count up every character of the first string, then "
                "count down every character of the second. At the end, all counts must be zero. For a "
                "small alphabet, an array of size 26 is enough; in general, use a hash map. Time is O of n, "
                "space O of 1 for the array version. The trade-off: sorting both strings costs O of n log n — "
                "counting is faster and simpler."
            ),
            "telugu": (
                "Pattern: frequency count. మొదటి string లో ప్రతి character count పెంచండి, రెండో string లో తగ్గించండి. "
                "చివర్లో అన్ని counts zero అవ్వాలి. చిన్న alphabet కోసం size 26 array సరిపోతుంది. "
                "Time complexity O(n). Sorting కన్నా ఇది fast మరియు simple."
            ),
            "tamil": (
                "Pattern: frequency count. முதல் string-ல் ஒவ்வொரு character count-ஐ கூட்டுங்கள், இரண்டாவது "
                "string-ல் குறையுங்கள். கடைசியில் எல்லா counts-உம் zero ஆக வேண்டும். சிறிய alphabet-க்கு size 26 "
                "array போதும். Time complexity O(n). Sorting-ஐ விட இது fast மற்றும் simple."
            ),
            "kannada": (
                "Pattern: frequency count. ಮೊದಲ string ನಲ್ಲಿ ಪ್ರತಿ character count ಹೆಚ್ಚಿಸಿ, ಎರಡನೇ string ನಲ್ಲಿ "
                "ಕಡಿಮೆ ಮಾಡಿ. ಕೊನೆಯಲ್ಲಿ ಎಲ್ಲಾ counts zero ಆಗಬೇಕು. ಚಿಕ್ಕ alphabet ಗೆ size 26 array ಸಾಕು. "
                "Time complexity O(n). Sorting ಕ್ಕಿಂತ ಇದು fast ಮತ್ತು simple."
            ),
            "malayalam": (
                "Pattern: frequency count. ആദ്യ string-ൽ ഓരോ character count-ഉം കൂട്ടുക, രണ്ടാമത്തെ string-ൽ "
                "കുറയ്ക്കുക. അവസാനം എല്ലാ counts-ഉം zero ആകണം. ചെറിയ alphabet-ന് size 26 array മതി. "
                "Time complexity O(n). Sorting-നേക്കാൾ ഇത് fast-ഉം simple-ഉം ആണ്."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: dono shabdon ke letters gino. Har letter ki ginti barabar ho toh anagram hai.",
            "english": "Simply: count the letters in both words. If every letter count matches, it's an anagram.",
        },
        "example": "Example: anagram aur nagaram. Dono mein a teen baar, aur g, n, r, m ek ek baar. Counts barabar — anagram hai.",
    },
    {
        "topic": "Sliding Window (generic)",
        "keywords": ["sliding window", "window pattern", "खिड़की",
                      "స్లైడింగ్ విండో", "ஸ்லைடிங் விண்டோ", "ಸ್ಲೈಡಿಂಗ್ ವಿಂಡೋ", "സ്ലൈഡിംഗ് വിൻഡോ"],
        "answers": {
            "hinglish": (
                "Sliding window tab use hota hai jab subarray ya substring par koi condition check karni ho "
                "aur array ke elements zyada tar positive hon ya window ka size manageable ho. "
                "Right pointer window failata hai, aur condition toot-te hi left pointer window sikodta hai. "
                "Dono pointers sirf aage badhte hain, isliye time O of n hota hai. "
                "Trade-off: negative numbers wale sum problems mein ye fail ho sakta hai, wahan prefix sum with hash map lagta hai."
            ),
            "english": (
                "Use a sliding window when you must check a condition over a subarray or substring and the "
                "elements are mostly positive, or the window size is manageable. The right pointer expands "
                "the window; when the condition breaks, the left pointer shrinks it. Both pointers only move "
                "forward, giving O of n time. The trade-off: with negative numbers in a sum problem this can "
                "fail — switch to prefix sum with a hash map there."
            ),
            "telugu": (
                "Subarray లేదా substring పై condition check చేయాల్సి వచ్చినప్పుడు sliding window వాడండి. "
                "Right pointer window ని విస్తరిస్తుంది, condition విరిగితే left pointer దాన్ని తగ్గిస్తుంది. "
                "రెండు pointers ముందుకే వెళ్తాయి కాబట్టి time O(n). Negative numbers ఉంటే prefix sum వాడాలి."
            ),
            "tamil": (
                "Subarray அல்லது substring மீது condition check செய்ய வேண்டியபோது sliding window பயன்படுத்துங்கள். "
                "Right pointer window-ஐ விரிவாக்கும், condition முறிந்தால் left pointer அதை சுருக்கும். "
                "இரண்டு pointers-உம் முன்னோக்கி மட்டுமே நகர்வதால் time O(n). Negative numbers இருந்தால் prefix sum வேண்டும்."
            ),
            "kannada": (
                "Subarray ಅಥವಾ substring ಮೇಲೆ condition check ಮಾಡಬೇಕಾದಾಗ sliding window ಬಳಸಿ. "
                "Right pointer window ಅನ್ನು ವಿಸ್ತರಿಸುತ್ತದೆ, condition ಮುರಿದರೆ left pointer ಅದನ್ನು ಕುಗ್ಗಿಸುತ್ತದೆ. "
                "ಎರಡು pointers ಮುಂದಕ್ಕೆ ಮಾತ್ರ ಚಲಿಸುವುದರಿಂದ time O(n). Negative numbers ಇದ್ದರೆ prefix sum ಬೇಕು."
            ),
            "malayalam": (
                "Subarray അല്ലെങ്കിൽ substring-മേൽ condition check ചെയ്യേണ്ടിവരുമ്പോൾ sliding window ഉപയോഗിക്കുക. "
                "Right pointer window വലുതാക്കും, condition തെറ്റിയാൽ left pointer ചുരുക്കും. "
                "രണ്ട് pointers-ഉം മുന്നോട്ട് മാത്രം നീങ്ങുന്നതുകൊണ്ട് time O(n). Negative numbers ഉണ്ടെങ്കിൽ prefix sum വേണം."
            ),
        },
        "simple": {
            "hinglish": "Simple mein: ek khidki jo aage badhti hai — right se failao, left se sikodo. Har element ek hi baar andar aur ek hi baar bahar.",
            "english": "Simply: a window that slides forward — grow it from the right, shrink it from the left. Every element enters and leaves once.",
        },
        "example": "Example: array hai 2, 1, 5, 1, 3, 2 aur k hai 3. Teen teen ki windows: 2 1 5 ka sum 8, 1 5 1 ka 7, 5 1 3 ka 9, 1 3 2 ka 6. Maximum 9 hai.",
    },
]

# --- Clarifying fallback (used when no topic matches) -----------------------

_TOPIC_LIST_EN = (
    "Two Sum, 3Sum, Container With Most Water, Stock Buy and Sell, Product of Array Except Self, "
    "Longest Consecutive Sequence, Prefix Sum, Remove Duplicates, Move Zeroes, Longest Substring, "
    "Valid Anagram, and the Sliding Window pattern"
)

FALLBACKS = {
    "hinglish": (
        "Ye sawal main pakad nahi paaya — thoda clarify karte hain. Kya tum in mein se kisi topic par "
        "pooch rahe ho: Two Sum, 3Sum, Container With Most Water, Stock Buy Sell, Product Except Self, "
        "Prefix Sum, Sliding Window ya Anagram? Topic ka naam bol do, main pattern ke saath samjha deta hoon."
    ),
    "english": (
        "I could not catch that question — let me clarify. Are you asking about one of these topics: "
        + _TOPIC_LIST_EN + "? Just say the topic name and I will explain it with its pattern."
    ),
    "telugu": (
        "ఆ ప్రశ్న నాకు అర్థం కాలేదు — కాస్త clarify చేద్దాం. మీరు ఈ topics లో దేని గురించైనా అడుగుతున్నారా: "
        "Two Sum, 3Sum, Stock Buy Sell, Prefix Sum, Sliding Window లేదా Anagram? Topic పేరు చెప్పండి, pattern తో వివరిస్తాను."
    ),
    "tamil": (
        "அந்த கேள்வி எனக்கு புரியவில்லை — கொஞ்சம் clarify செய்வோம். இந்த topics-ல் ஏதாவது ஒன்றைப் பற்றி "
        "கேட்கிறீர்களா: Two Sum, 3Sum, Stock Buy Sell, Prefix Sum, Sliding Window அல்லது Anagram? "
        "Topic பெயரைச் சொல்லுங்கள், pattern உடன் விளக்குகிறேன்."
    ),
    "kannada": (
        "ಆ ಪ್ರಶ್ನೆ ನನಗೆ ಸಿಗಲಿಲ್ಲ — ಸ್ವಲ್ಪ clarify ಮಾಡೋಣ. ನೀವು ಈ topics ಗಳಲ್ಲಿ ಯಾವುದಾದರೂ ಒಂದರ ಬಗ್ಗೆ "
        "ಕೇಳುತ್ತಿದ್ದೀರಾ: Two Sum, 3Sum, Stock Buy Sell, Prefix Sum, Sliding Window ಅಥವಾ Anagram? "
        "Topic ಹೆಸರು ಹೇಳಿ, pattern ಜೊತೆಗೆ ವಿವರಿಸುತ್ತೇನೆ."
    ),
    "malayalam": (
        "ആ ചോദ്യം എനിക്ക് പിടികിട്ടിയില്ല — അല്പം clarify ചെയ്യാം. ഈ topics-ൽ ഏതെങ്കിലും ഒന്നിനെക്കുറിച്ചാണോ "
        "ചോദിക്കുന്നത്: Two Sum, 3Sum, Stock Buy Sell, Prefix Sum, Sliding Window അല്ലെങ്കിൽ Anagram? "
        "Topic-ന്റെ പേര് പറയുക, pattern സഹിതം വിശദീകരിക്കാം."
    ),
}

# --- Transcript normalisation ------------------------------------------------
# Prisma may return Devanagari/native-script words, and can mishear English
# terms spoken in Indian languages. Normalise common aliases before matching.

ALIASES = {
    "डू": "two", "टू": "two", "थ्री": "three", "त्री": "three", "सम": "sum",
    "स्टॉक": "stock", "शेयर": "share", "पानी": "water", "डुप्लिकेट": "duplicate",
    "ज़ीरो": "zero", "शून्य": "zero", "सबएरे": "subarray", "एनाग्राम": "anagram",
    "प्रोडक्ट": "product", "कंटेनर": "container", "प्रॉफिट": "profit",
    "खरीदें": "buy", "बेचें": "sell",
    "టూ": "two", "సమ్": "sum", "స్టాక్": "stock", "షేర్": "share",
    "டூ": "two", "சம்": "sum", "ஸ்டாக்": "stock", "ஷேர்": "share",
    "ಟೂ": "two", "ಸಮ್": "sum", "ಸ್ಟಾಕ್": "stock", "ಶೇರ್": "share",
    "ടൂ": "two", "സം": "sum", "സ്റ്റോക്ക്": "stock", "ഷെയർ": "share",
}


def _normalize(text: str) -> str:
    tokens = (text or "").lower().split()
    return " ".join(ALIASES.get(tok, tok) for tok in tokens)


def _entry_for_topic(topic: str):
    for entry in ANSWERS:
        if entry["topic"] == topic:
            return entry
    return None


def find_answer(transcript: str, lang: str = "hinglish") -> tuple[str, str]:
    """Return (topic, answer_text) for a spoken/typed question in `lang`."""
    text = _normalize(transcript)
    best = None
    for entry in ANSWERS:
        for kw in entry["keywords"]:
            if kw.lower() in text or kw.lower() in (transcript or "").lower():
                if best is None or len(kw) > best[0]:
                    best = (len(kw), entry)
                break
    bank = answer_lang_for(lang)
    if best:
        entry = best[1]
        return entry["topic"], entry["answers"][bank]
    return "Not in list", FALLBACKS[bank]


def find_followup(topic: str, kind: str, lang: str = "hinglish") -> str:
    """Clarifying follow-ups: kind is 'simple' or 'example'."""
    entry = _entry_for_topic(topic)
    if entry is None:
        bank = answer_lang_for(lang)
        return FALLBACKS[bank]
    if kind == "example":
        return entry["example"]
    bank = answer_lang_for(lang)
    simple = entry["simple"]
    return simple.get(bank) or simple["english"]


def topics() -> list[str]:
    return [e["topic"] for e in ANSWERS]
