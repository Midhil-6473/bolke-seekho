"""Bolke Seekho approaches bank — key code, all approaches, best pick.

Each algorithm entry carries:
  name       — display name (matches the spoken-answer bank in answers.py
               where one exists, so voice follow-ups can reuse it)
  category   — family the algorithm belongs to
  aliases    — extra phrases that should match this algorithm (the spoken
               bank's keywords are merged in automatically at import)
  key_logic  — the one core idea, in one or two sentences
  approaches — every standard way to solve it, each with the key logic,
               the core Java code (a method, not a full program; assume
               `import java.util.*;`), time/space complexity, and exactly
               one approach flagged optimal (the best technique to use).

Anything not in this bank is answered by the configured LLM in the same
shape (see llm.py), so a student can search for ANY DSA algorithm.
"""

import difflib
import re

from answers import ANSWERS as _BANK_ENTRIES

ALGORITHMS = [
    {
        "name": "Two Sum",
        "category": "Arrays & Searching",
        "aliases": ["two sum", "2 sum", "pair sum", "target sum", "two numbers sum"],
        "key_logic": "Find two numbers that add up to the target. The trick is remembering numbers you have already seen, so each lookup is instant.",
        "approaches": [
            {
                "name": "Brute force",
                "logic": "Check every pair of numbers until one adds up to the target. Simple, but repeats the same comparisons.",
                "code": """
int[] twoSum(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++)
        for (int j = i + 1; j < nums.length; j++)
            if (nums[i] + nums[j] == target)
                return new int[]{i, j};
    return new int[]{-1, -1};
}""",
                "time": "O(n²)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Hash map",
                "logic": "One pass: for each number, check whether its partner (target minus current) was already seen. The map remembers past numbers, so no re-searching.",
                "code": """
int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int need = target - nums[i];
        if (seen.containsKey(need))
            return new int[]{seen.get(need), i};
        seen.put(nums[i], i);
    }
    return new int[]{-1, -1};
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": True,
            },
            {
                "name": "Two pointers (sorted array)",
                "logic": "Sort first, then squeeze from both ends: sum too small, move left; too big, move right. Loses the original indices, so only use it when the values (not positions) matter.",
                "code": """
// Works on a SORTED array; original indices are lost.
int[] twoSum(int[] nums, int target) {
    int l = 0, r = nums.length - 1;
    while (l < r) {
        int sum = nums[l] + nums[r];
        if (sum == target) return new int[]{l, r};
        if (sum < target) l++; else r--;
    }
    return new int[]{-1, -1};
}""",
                "time": "O(n log n)",
                "space": "O(1)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "3Sum",
        "category": "Arrays & Searching",
        "aliases": ["3sum", "three sum", "triplet sum zero", "3 sum"],
        "key_logic": "Find all unique triplets that sum to zero. Sort first, then fix one number and two-pointer the rest.",
        "approaches": [
            {
                "name": "Brute force",
                "logic": "Three nested loops try every triplet, then a set removes duplicates. Easy to write, far too slow for interviews.",
                "code": """
List<List<Integer>> threeSum(int[] nums) {
    Set<List<Integer>> found = new HashSet<>();
    for (int i = 0; i < nums.length; i++)
        for (int j = i + 1; j < nums.length; j++)
            for (int k = j + 1; k < nums.length; k++)
                if (nums[i] + nums[j] + nums[k] == 0) {
                    List<Integer> t = Arrays.asList(nums[i], nums[j], nums[k]);
                    Collections.sort(t);
                    found.add(t);
                }
    return new ArrayList<>(found);
}""",
                "time": "O(n³)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Sort + two pointers",
                "logic": "Sort, fix the first number, then squeeze the other two with pointers. Skipping equal neighbours removes duplicates without a set.",
                "code": """
List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> ans = new ArrayList<>();
    for (int i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        int l = i + 1, r = nums.length - 1;
        while (l < r) {
            int sum = nums[i] + nums[l] + nums[r];
            if (sum == 0) {
                ans.add(List.of(nums[i], nums[l], nums[r]));
                while (l < r && nums[l] == nums[l + 1]) l++;
                while (l < r && nums[r] == nums[r - 1]) r--;
                l++; r--;
            } else if (sum < 0) l++;
            else r--;
        }
    }
    return ans;
}""",
                "time": "O(n²)",
                "space": "O(1)",
                "optimal": True,
            },
            {
                "name": "Hash set pairs",
                "logic": "Fix the first number, then use a hash set to find pairs summing to its negative. Same time as two pointers but needs extra memory and a set for dedup.",
                "code": """
List<List<Integer>> threeSum(int[] nums) {
    Set<List<Integer>> found = new HashSet<>();
    for (int i = 0; i < nums.length; i++) {
        Set<Integer> seen = new HashSet<>();
        for (int j = i + 1; j < nums.length; j++) {
            int need = -(nums[i] + nums[j]);
            if (seen.contains(need)) {
                List<Integer> t = Arrays.asList(nums[i], nums[j], need);
                Collections.sort(t);
                found.add(t);
            }
            seen.add(nums[j]);
        }
    }
    return new ArrayList<>(found);
}""",
                "time": "O(n²)",
                "space": "O(n)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Container With Most Water",
        "category": "Arrays & Searching",
        "aliases": ["container with most water", "most water", "max water container", "trapping water container"],
        "key_logic": "Two lines hold water: area equals distance times the shorter line. Start wide, and always move the shorter side — moving the taller side can never help.",
        "approaches": [
            {
                "name": "Brute force",
                "logic": "Compute the area for every pair of lines and keep the biggest. Correct but quadratic.",
                "code": """
int maxArea(int[] height) {
    int best = 0;
    for (int i = 0; i < height.length; i++)
        for (int j = i + 1; j < height.length; j++)
            best = Math.max(best, (j - i) * Math.min(height[i], height[j]));
    return best;
}""",
                "time": "O(n²)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Two pointers",
                "logic": "Start at both ends (widest container). Record the area, then move the shorter line inward — only a taller line can beat the current area.",
                "code": """
int maxArea(int[] height) {
    int l = 0, r = height.length - 1, best = 0;
    while (l < r) {
        best = Math.max(best, (r - l) * Math.min(height[l], height[r]));
        if (height[l] < height[r]) l++; else r--;
    }
    return best;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Best Time to Buy and Sell Stock",
        "category": "Arrays & Searching",
        "aliases": ["buy sell stock", "best time buy sell", "stock profit", "maximum profit stock"],
        "key_logic": "Track the lowest price seen so far; the best profit today is today's price minus that minimum. One pass is enough.",
        "approaches": [
            {
                "name": "Brute force",
                "logic": "Try every buy day with every later sell day and keep the best profit. Simple, quadratic.",
                "code": """
int maxProfit(int[] prices) {
    int best = 0;
    for (int i = 0; i < prices.length; i++)
        for (int j = i + 1; j < prices.length; j++)
            best = Math.max(best, prices[j] - prices[i]);
    return best;
}""",
                "time": "O(n²)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "One pass (track minimum)",
                "logic": "Walk once, remembering the cheapest price so far. Each day, either update the cheapest price or record a better profit.",
                "code": """
int maxProfit(int[] prices) {
    int cheapest = Integer.MAX_VALUE, best = 0;
    for (int p : prices) {
        cheapest = Math.min(cheapest, p);
        best = Math.max(best, p - cheapest);
    }
    return best;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Product of Array Except Self",
        "category": "Arrays & Searching",
        "aliases": ["product except self", "product of array except self", "product without division"],
        "key_logic": "Each answer is (product of everything to the left) times (product of everything to the right). Two passes, no division — so zeroes never break it.",
        "approaches": [
            {
                "name": "Division",
                "logic": "Multiply everything, then divide by each element. Breaks the moment the array contains a zero (and division is banned by the problem).",
                "code": """
// WRONG when any element is zero. Shown only to explain why not.
int[] productExceptSelf(int[] nums) {
    int total = 1;
    for (int n : nums) total *= n;
    int[] ans = new int[nums.length];
    for (int i = 0; i < nums.length; i++) ans[i] = total / nums[i];
    return ans;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Prefix and suffix arrays",
                "logic": "Build a left-products array and a right-products array, then multiply them per index. Clear, but uses two extra arrays.",
                "code": """
int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] left = new int[n], right = new int[n], ans = new int[n];
    left[0] = 1;
    for (int i = 1; i < n; i++) left[i] = left[i - 1] * nums[i - 1];
    right[n - 1] = 1;
    for (int i = n - 2; i >= 0; i--) right[i] = right[i + 1] * nums[i + 1];
    for (int i = 0; i < n; i++) ans[i] = left[i] * right[i];
    return ans;
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Output array + running products",
                "logic": "Store left products in the answer array, then sweep back multiplying in the right products with a single running variable. No extra arrays.",
                "code": """
int[] productExceptSelf(int[] nums) {
    int n = nums.length, ans[] = new int[n];
    ans[0] = 1;
    for (int i = 1; i < n; i++) ans[i] = ans[i - 1] * nums[i - 1];
    int right = 1;
    for (int i = n - 1; i >= 0; i--) {
        ans[i] *= right;
        right *= nums[i];
    }
    return ans;
}""",
                "time": "O(n)",
                "space": "O(1) extra",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Longest Consecutive Sequence",
        "category": "Arrays & Searching",
        "aliases": ["longest consecutive", "consecutive sequence", "longest consecutive sequence"],
        "key_logic": "Only start counting from numbers that begin a run (no n−1 present), so each run is walked exactly once.",
        "approaches": [
            {
                "name": "Brute force",
                "logic": "For every number, walk forward checking each next number with a linear search. The same runs get rescanned again and again.",
                "code": """
int longestConsecutive(int[] nums) {
    int best = 0;
    for (int n : nums) {
        int cur = n, len = 1;
        while (contains(nums, cur + 1)) { cur++; len++; }
        best = Math.max(best, len);
    }
    return best;
}
boolean contains(int[] nums, int x) {
    for (int n : nums) if (n == x) return true;
    return false;
}""",
                "time": "O(n³)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Sort first",
                "logic": "Sort, then one pass counts runs of consecutive values, skipping duplicates. The sort dominates the time.",
                "code": """
int longestConsecutive(int[] nums) {
    if (nums.length == 0) return 0;
    Arrays.sort(nums);
    int best = 1, len = 1;
    for (int i = 1; i < nums.length; i++) {
        if (nums[i] == nums[i - 1]) continue;
        if (nums[i] == nums[i - 1] + 1) len++;
        else len = 1;
        best = Math.max(best, len);
    }
    return best;
}""",
                "time": "O(n log n)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Hash set",
                "logic": "Put everything in a set. Only start a run at numbers with no predecessor in the set, then walk forward with O(1) lookups.",
                "code": """
int longestConsecutive(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int n : nums) set.add(n);
    int best = 0;
    for (int n : set) {
        if (!set.contains(n - 1)) {
            int cur = n, len = 1;
            while (set.contains(cur + 1)) { cur++; len++; }
            best = Math.max(best, len);
        }
    }
    return best;
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Subarray Sum Equals K (Prefix Sum)",
        "category": "Arrays & Searching",
        "aliases": ["subarray sum equals k", "subarray sum k", "subarrays divisible", "count subarrays sum k", "prefix sum subarray"],
        "key_logic": "Prefix sums turn 'subarray sums to k' into 'have I seen prefix minus k before?' — one hash map pass answers it, even with negative numbers.",
        "approaches": [
            {
                "name": "Brute force",
                "logic": "Check every subarray's sum directly. Works, but quadratic and easy to beat.",
                "code": """
int subarraySum(int[] nums, int k) {
    int count = 0;
    for (int i = 0; i < nums.length; i++) {
        int sum = 0;
        for (int j = i; j < nums.length; j++) {
            sum += nums[j];
            if (sum == k) count++;
        }
    }
    return count;
}""",
                "time": "O(n²)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Prefix sum + hash map",
                "logic": "Track the running prefix sum. If (prefix − k) appeared before, every occurrence ends a valid subarray here. Count frequencies in the map.",
                "code": """
int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    freq.put(0, 1);
    int sum = 0, count = 0;
    for (int n : nums) {
        sum += n;
        count += freq.getOrDefault(sum - k, 0);
        freq.put(sum, freq.getOrDefault(sum, 0) + 1);
    }
    return count;
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Remove Duplicates from Sorted Array",
        "category": "Arrays & Searching",
        "aliases": ["remove duplicates", "remove duplicates sorted", "deduplicate sorted array"],
        "key_logic": "The array is sorted, so duplicates sit together. One slow pointer marks the next unique slot; one fast pointer scans.",
        "approaches": [
            {
                "name": "Extra array",
                "logic": "Copy unique values into a new array, then copy back. Simple but uses extra memory the problem asks you to avoid.",
                "code": """
int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;
    int[] copy = new int[nums.length];
    int w = 0;
    for (int i = 0; i < nums.length; i++)
        if (i == 0 || nums[i] != nums[i - 1]) copy[w++] = nums[i];
    System.arraycopy(copy, 0, nums, 0, w);
    return w;
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Two pointers in place",
                "logic": "The slow pointer only advances when the fast pointer finds a new value. Everything before the slow pointer is the deduped answer.",
                "code": """
int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;
    int slow = 0;
    for (int fast = 1; fast < nums.length; fast++)
        if (nums[fast] != nums[slow])
            nums[++slow] = nums[fast];
    return slow + 1;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Move Zeroes",
        "category": "Arrays & Searching",
        "aliases": ["move zeroes", "move zeros", "move zeroes to end", "shift zeroes"],
        "key_logic": "Compact all non-zeroes to the front in order, then fill the tail with zeroes. Relative order of non-zeroes must stay the same.",
        "approaches": [
            {
                "name": "Extra array",
                "logic": "Collect non-zeroes into a new array, copy back, zero-fill the rest. Clear, but extra memory.",
                "code": """
void moveZeroes(int[] nums) {
    int[] copy = new int[nums.length];
    int w = 0;
    for (int n : nums) if (n != 0) copy[w++] = n;
    System.arraycopy(copy, 0, nums, 0, nums.length);
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Two pointers (overwrite)",
                "logic": "Write each non-zero to the next front slot, then zero-fill the tail. One pass plus a fill — the cleanest in-place version.",
                "code": """
void moveZeroes(int[] nums) {
    int w = 0;
    for (int n : nums) if (n != 0) nums[w++] = n;
    while (w < nums.length) nums[w++] = 0;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
            {
                "name": "Swap in place",
                "logic": "Swap each non-zero forward into the next slot. Same complexity, single pass, but writes more often than overwriting.",
                "code": """
void moveZeroes(int[] nums) {
    int w = 0;
    for (int r = 0; r < nums.length; r++)
        if (nums[r] != 0) {
            int tmp = nums[w]; nums[w] = nums[r]; nums[r] = tmp;
            w++;
        }
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Longest Substring Without Repeating Characters",
        "category": "Strings & Hashing",
        "aliases": ["longest substring without repeating", "longest substring no repeat", "longest unique substring"],
        "key_logic": "A sliding window holds the current substring; when a repeat enters, shrink from the left until it is unique again.",
        "approaches": [
            {
                "name": "Brute force",
                "logic": "Generate every substring and check each for repeats with a set. Correct, cubic, never the interview answer.",
                "code": """
int lengthOfLongestSubstring(String s) {
    int best = 0;
    for (int i = 0; i < s.length(); i++)
        for (int j = i; j < s.length(); j++)
            if (allUnique(s, i, j)) best = Math.max(best, j - i + 1);
    return best;
}
boolean allUnique(String s, int l, int r) {
    Set<Character> seen = new HashSet<>();
    for (int i = l; i <= r; i++)
        if (!seen.add(s.charAt(i))) return false;
    return true;
}""",
                "time": "O(n³)",
                "space": "O(min(n, m))",
                "optimal": False,
            },
            {
                "name": "Sliding window + set",
                "logic": "Expand the right edge; if the character is already in the set, shrink the left edge until it is not. Each character enters and leaves once.",
                "code": """
int lengthOfLongestSubstring(String s) {
    Set<Character> window = new HashSet<>();
    int best = 0, l = 0;
    for (int r = 0; r < s.length(); r++) {
        while (window.contains(s.charAt(r)))
            window.remove(s.charAt(l++));
        window.add(s.charAt(r));
        best = Math.max(best, r - l + 1);
    }
    return best;
}""",
                "time": "O(n)",
                "space": "O(min(n, m))",
                "optimal": False,
            },
            {
                "name": "Sliding window + index map",
                "logic": "Remember each character's last index. On a repeat, jump the left edge straight past the previous occurrence instead of shrinking one by one.",
                "code": """
int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> last = new HashMap<>();
    int best = 0, l = 0;
    for (int r = 0; r < s.length(); r++) {
        char c = s.charAt(r);
        if (last.containsKey(c)) l = Math.max(l, last.get(c) + 1);
        last.put(c, r);
        best = Math.max(best, r - l + 1);
    }
    return best;
}""",
                "time": "O(n)",
                "space": "O(min(n, m))",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Valid Anagram",
        "category": "Strings & Hashing",
        "aliases": ["valid anagram", "anagram check", "check anagram", "are anagrams"],
        "key_logic": "Two strings are anagrams when their letter counts match exactly. Count, don't rearrange.",
        "approaches": [
            {
                "name": "Sort both strings",
                "logic": "Anagrams become identical once sorted. Simple and obviously correct; the sort costs the most.",
                "code": """
boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    char[] a = s.toCharArray(), b = t.toCharArray();
    Arrays.sort(a); Arrays.sort(b);
    return Arrays.equals(a, b);
}""",
                "time": "O(n log n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Frequency array",
                "logic": "Count each letter in the first string, subtract for the second. All zeroes means anagram. Fixed 26 slots, so constant space.",
                "code": """
boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] count = new int[26];
    for (int i = 0; i < s.length(); i++) {
        count[s.charAt(i) - 'a']++;
        count[t.charAt(i) - 'a']--;
    }
    for (int c : count) if (c != 0) return false;
    return true;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
            {
                "name": "Hash map counts",
                "logic": "Same counting idea with a map, so it works for any Unicode characters, not just lowercase letters. Slightly more overhead.",
                "code": """
boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    Map<Character, Integer> count = new HashMap<>();
    for (char c : s.toCharArray())
        count.put(c, count.getOrDefault(c, 0) + 1);
    for (char c : t.toCharArray()) {
        count.put(c, count.getOrDefault(c, 0) - 1);
        if (count.get(c) == 0) count.remove(c);
    }
    return count.isEmpty();
}""",
                "time": "O(n)",
                "space": "O(k)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Sliding Window (generic)",
        "category": "Arrays & Searching",
        "aliases": ["sliding window", "sliding window technique", "window technique", "two pointers window"],
        "key_logic": "A window slides across the array instead of recomputing from scratch: add the entering element, remove the leaving one. Each element is touched twice at most.",
        "approaches": [
            {
                "name": "Recompute every window",
                "logic": "For each window position, sum or scan the whole window again. The same elements get re-added hundreds of times.",
                "code": """
// Max sum of any k consecutive elements, the slow way.
int maxSum(int[] nums, int k) {
    int best = Integer.MIN_VALUE;
    for (int i = 0; i + k <= nums.length; i++) {
        int sum = 0;
        for (int j = i; j < i + k; j++) sum += nums[j];
        best = Math.max(best, sum);
    }
    return best;
}""",
                "time": "O(n·k)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Fixed-size window",
                "logic": "Sum the first window, then slide: add the new element, subtract the one that left. Use it when the window size is fixed (k elements).",
                "code": """
int maxSum(int[] nums, int k) {
    int sum = 0;
    for (int i = 0; i < k; i++) sum += nums[i];
    int best = sum;
    for (int i = k; i < nums.length; i++) {
        sum += nums[i] - nums[i - k];
        best = Math.max(best, sum);
    }
    return best;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Variable-size window",
                "logic": "Expand the right edge, and shrink the left edge while the window breaks the rule. The general pattern behind longest-substring, minimum-window, and most subarray problems.",
                "code": """
// Longest subarray whose sum is at most k (positive numbers).
int longestAtMost(int[] nums, int k) {
    int best = 0, sum = 0, l = 0;
    for (int r = 0; r < nums.length; r++) {
        sum += nums[r];
        while (sum > k) sum -= nums[l++];
        best = Math.max(best, r - l + 1);
    }
    return best;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Binary Search",
        "category": "Arrays & Searching",
        "aliases": ["binary search", "binarysearch", "search sorted array"],
        "key_logic": "Sorted data halves the search space every step: compare with the middle, discard the wrong half. Log time needs sorted input.",
        "approaches": [
            {
                "name": "Linear scan",
                "logic": "Check each element in order. Works on unsorted data too, but wastes the sorted order completely.",
                "code": """
int search(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++)
        if (nums[i] == target) return i;
    return -1;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Iterative binary search",
                "logic": "Keep a [low, high] range, check the middle, keep the half that can contain the target. No recursion overhead.",
                "code": """
int search(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2; // avoids overflow
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}""",
                "time": "O(log n)",
                "space": "O(1)",
                "optimal": True,
            },
            {
                "name": "Recursive binary search",
                "logic": "Same halving idea expressed as recursion: search the left or right half. Elegant, but each call costs stack space.",
                "code": """
int search(int[] nums, int target) {
    return search(nums, target, 0, nums.length - 1);
}
int search(int[] nums, int target, int lo, int hi) {
    if (lo > hi) return -1;
    int mid = lo + (hi - lo) / 2;
    if (nums[mid] == target) return mid;
    if (nums[mid] < target) return search(nums, target, mid + 1, hi);
    return search(nums, target, lo, mid - 1);
}""",
                "time": "O(log n)",
                "space": "O(log n)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Merge Intervals",
        "category": "Arrays & Searching",
        "aliases": ["merge intervals", "merge overlapping intervals", "overlapping intervals"],
        "key_logic": "Sort by start time; overlapping intervals then sit next to each other and merge in one pass.",
        "approaches": [
            {
                "name": "Pairwise merging",
                "logic": "Repeatedly scan for any two overlapping intervals and merge them until none overlap. Works, but rescans constantly.",
                "code": """
// Sketch: repeat until stable — merge any overlapping pair found.
List<int[]> merge(List<int[]> intervals) {
    boolean changed = true;
    while (changed) {
        changed = false;
        outer:
        for (int i = 0; i < intervals.size(); i++)
            for (int j = i + 1; j < intervals.size(); j++) {
                int[] a = intervals.get(i), b = intervals.get(j);
                if (a[0] <= b[1] && b[0] <= a[1]) {
                    intervals.set(i, new int[]{Math.min(a[0], b[0]), Math.max(a[1], b[1])});
                    intervals.remove(j);
                    changed = true;
                    break outer;
                }
            }
    }
    return intervals;
}""",
                "time": "O(n²)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Sort + single pass",
                "logic": "Sort by start. Keep the last merged interval: if the next one starts before it ends, extend it; otherwise start a new one.",
                "code": """
int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
    List<int[]> merged = new ArrayList<>();
    for (int[] in : intervals) {
        if (merged.isEmpty() || in[0] > merged.get(merged.size() - 1)[1])
            merged.add(new int[]{in[0], in[1]});
        else
            merged.get(merged.size() - 1)[1] =
                Math.max(merged.get(merged.size() - 1)[1], in[1]);
    }
    return merged.toArray(new int[0][]);
}""",
                "time": "O(n log n)",
                "space": "O(n)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Trapping Rain Water",
        "category": "Arrays & Searching",
        "aliases": ["trapping rain water", "rain water trapped", "trap rainwater", "trapped water"],
        "key_logic": "Water over a bar equals min(highest bar on the left, highest on the right) minus the bar's own height, never below zero.",
        "approaches": [
            {
                "name": "Brute force",
                "logic": "For each bar, scan left and right to find the highest bars. Recomputes the same maxima for every position.",
                "code": """
int trap(int[] height) {
    int water = 0;
    for (int i = 0; i < height.length; i++) {
        int leftMax = 0, rightMax = 0;
        for (int j = 0; j <= i; j++) leftMax = Math.max(leftMax, height[j]);
        for (int j = i; j < height.length; j++) rightMax = Math.max(rightMax, height[j]);
        water += Math.min(leftMax, rightMax) - height[i];
    }
    return water;
}""",
                "time": "O(n²)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "DP arrays",
                "logic": "Precompute the highest bar to the left and right of every position once, then one pass applies the formula. Fast, but two extra arrays.",
                "code": """
int trap(int[] height) {
    int n = height.length, water = 0;
    int[] leftMax = new int[n], rightMax = new int[n];
    for (int i = 1; i < n; i++) leftMax[i] = Math.max(leftMax[i - 1], height[i - 1]);
    for (int i = n - 2; i >= 0; i--) rightMax[i] = Math.max(rightMax[i + 1], height[i + 1]);
    for (int i = 0; i < n; i++)
        water += Math.max(0, Math.min(leftMax[i], rightMax[i]) - height[i]);
    return water;
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Two pointers",
                "logic": "Squeeze from both ends tracking the highest bar seen on each side. The lower side decides the water level, so one pass with no arrays is enough.",
                "code": """
int trap(int[] height) {
    int l = 0, r = height.length - 1, leftMax = 0, rightMax = 0, water = 0;
    while (l < r) {
        if (height[l] < height[r]) {
            leftMax = Math.max(leftMax, height[l]);
            water += leftMax - height[l++];
        } else {
            rightMax = Math.max(rightMax, height[r]);
            water += rightMax - height[r--];
        }
    }
    return water;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Maximum Subarray (Kadane's Algorithm)",
        "category": "Arrays & Searching",
        "aliases": ["maximum subarray", "kadane", "kadane's algorithm", "max subarray sum", "largest sum subarray"],
        "key_logic": "Keep a running sum; if it ever goes negative, restart from the next element — a negative prefix only drags the total down.",
        "approaches": [
            {
                "name": "Brute force",
                "logic": "Sum every possible subarray and keep the largest. Straightforward, quadratic.",
                "code": """
int maxSubArray(int[] nums) {
    int best = Integer.MIN_VALUE;
    for (int i = 0; i < nums.length; i++) {
        int sum = 0;
        for (int j = i; j < nums.length; j++) {
            sum += nums[j];
            best = Math.max(best, sum);
        }
    }
    return best;
}""",
                "time": "O(n²)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Divide and conquer",
                "logic": "Split the array; the answer is the best in the left half, the right half, or crossing the middle. Elegant recursion, slower than Kadane's.",
                "code": """
int maxSubArray(int[] nums) { return solve(nums, 0, nums.length - 1); }
int solve(int[] nums, int l, int r) {
    if (l == r) return nums[l];
    int m = (l + r) / 2;
    int leftSum = Integer.MIN_VALUE, sum = 0;
    for (int i = m; i >= l; i--) { sum += nums[i]; leftSum = Math.max(leftSum, sum); }
    int rightSum = Integer.MIN_VALUE; sum = 0;
    for (int i = m + 1; i <= r; i++) { sum += nums[i]; rightSum = Math.max(rightSum, sum); }
    return Math.max(Math.max(solve(nums, l, m), solve(nums, m + 1, r)), leftSum + rightSum);
}""",
                "time": "O(n log n)",
                "space": "O(log n)",
                "optimal": False,
            },
            {
                "name": "Kadane's algorithm",
                "logic": "At each element decide: extend the current subarray or start fresh here. Track the best seen. One pass, two variables.",
                "code": """
int maxSubArray(int[] nums) {
    int current = nums[0], best = nums[0];
    for (int i = 1; i < nums.length; i++) {
        current = Math.max(nums[i], current + nums[i]);
        best = Math.max(best, current);
    }
    return best;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Group Anagrams",
        "category": "Strings & Hashing",
        "aliases": ["group anagrams", "grouping anagrams", "anagram groups"],
        "key_logic": "Anagrams share a signature: either the sorted word or its 26 letter counts. Group words by their signature.",
        "approaches": [
            {
                "name": "Sort each word",
                "logic": "Sort the letters of every word; anagrams produce the same sorted key. Group by that key in a map.",
                "code": """
List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String s : strs) {
        char[] chars = s.toCharArray();
        Arrays.sort(chars);
        String key = new String(chars);
        groups.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}""",
                "time": "O(n·k log k)",
                "space": "O(n·k)",
                "optimal": False,
            },
            {
                "name": "Count signature",
                "logic": "Build a 26-count signature per word instead of sorting — counting is linear in word length, so the sort factor disappears.",
                "code": """
List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String s : strs) {
        int[] count = new int[26];
        for (char c : s.toCharArray()) count[c - 'a']++;
        String key = Arrays.toString(count);
        groups.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}""",
                "time": "O(n·k)",
                "space": "O(n·k)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Longest Palindromic Substring",
        "category": "Strings & Hashing",
        "aliases": ["longest palindromic substring", "longest palindrome", "palindromic substring"],
        "key_logic": "A palindrome mirrors around its centre. Expand outwards from every possible centre and keep the longest expansion.",
        "approaches": [
            {
                "name": "Brute force",
                "logic": "Check every substring for being a palindrome. n² substrings, each check up to n — cubic and only a starting point.",
                "code": """
String longestPalindrome(String s) {
    String best = "";
    for (int i = 0; i < s.length(); i++)
        for (int j = i; j < s.length(); j++) {
            String sub = s.substring(i, j + 1);
            if (isPalindrome(sub) && sub.length() > best.length()) best = sub;
        }
    return best;
}
boolean isPalindrome(String s) {
    int l = 0, r = s.length() - 1;
    while (l < r) if (s.charAt(l++) != s.charAt(r--)) return false;
    return true;
}""",
                "time": "O(n³)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Expand around center",
                "logic": "Treat every position (and every gap) as a centre and expand while characters match. Two centre types cover odd and even palindromes.",
                "code": """
String longestPalindrome(String s) {
    int start = 0, len = 0;
    for (int i = 0; i < s.length(); i++) {
        int odd = expand(s, i, i), even = expand(s, i, i + 1);
        int cur = Math.max(odd, even);
        if (cur > len) { len = cur; start = i - (cur - 1) / 2; }
    }
    return s.substring(start, start + len);
}
int expand(String s, int l, int r) {
    while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
    return r - l - 1;
}""",
                "time": "O(n²)",
                "space": "O(1)",
                "optimal": True,
            },
            {
                "name": "DP table",
                "logic": "A substring is a palindrome if its ends match and the inside is a palindrome. Fill a table of known results bottom-up.",
                "code": """
String longestPalindrome(String s) {
    int n = s.length(), start = 0, len = 1;
    boolean[][] dp = new boolean[n][n];
    for (int i = n - 1; i >= 0; i--) {
        dp[i][i] = true;
        for (int j = i + 1; j < n; j++) {
            dp[i][j] = s.charAt(i) == s.charAt(j) && (j - i < 2 || dp[i + 1][j - 1]);
            if (dp[i][j] && j - i + 1 > len) { start = i; len = j - i + 1; }
        }
    }
    return s.substring(start, start + len);
}""",
                "time": "O(n²)",
                "space": "O(n²)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Reverse Linked List",
        "category": "Linked List",
        "aliases": ["reverse linked list", "reverse a linked list", "reverse list", "linked list reverse"],
        "key_logic": "Walk the list flipping each node's arrow; three pointers (prev, curr, next) keep you from losing the rest of the list.",
        "approaches": [
            {
                "name": "Iterative (three pointers)",
                "logic": "Save the next node, flip the current arrow to point backwards, step all pointers forward. Constant extra space.",
                "code": """
ListNode reverseList(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode next = curr.next; // save before flipping
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
            {
                "name": "Recursive",
                "logic": "Reverse the rest of the list, then fix the current node's arrow. Same idea, expressed recursively — the call stack holds the pointers.",
                "code": """
ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode rest = reverseList(head.next);
    head.next.next = head;
    head.next = null;
    return rest;
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Stack",
                "logic": "Push all nodes on a stack, then pop them to rebuild the list in reverse order. Simple to reason about, wastes a full stack of space.",
                "code": """
ListNode reverseList(ListNode head) {
    Deque<ListNode> stack = new ArrayDeque<>();
    while (head != null) { stack.push(head); head = head.next; }
    ListNode dummy = new ListNode(0), curr = dummy;
    while (!stack.isEmpty()) { curr.next = stack.pop(); curr = curr.next; }
    curr.next = null;
    return dummy.next;
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Linked List Cycle",
        "category": "Linked List",
        "aliases": ["linked list cycle", "detect cycle", "cycle in linked list", "loop in linked list", "floyd cycle"],
        "key_logic": "Two runners at different speeds on a loop must eventually meet; on a straight road the fast one reaches the end. That meeting is the cycle test.",
        "approaches": [
            {
                "name": "Hash set of visited nodes",
                "logic": "Remember every node visited; the first repeat proves a cycle. Easy to see, but stores the whole list.",
                "code": """
boolean hasCycle(ListNode head) {
    Set<ListNode> seen = new HashSet<>();
    while (head != null) {
        if (!seen.add(head)) return true;
        head = head.next;
    }
    return false;
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Floyd's tortoise and hare",
                "logic": "A slow pointer moves one step, a fast pointer two. If they ever land on the same node, there is a cycle; if fast hits null, there is none.",
                "code": """
boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Merge Two Sorted Lists",
        "category": "Linked List",
        "aliases": ["merge two sorted lists", "merge sorted lists", "merge two lists"],
        "key_logic": "Always attach the smaller head node; a dummy node removes the empty-list edge case entirely.",
        "approaches": [
            {
                "name": "Dummy node + iterative",
                "logic": "Walk both lists with a tail pointer, attaching the smaller head each time, then attach whichever list remains.",
                "code": """
ListNode mergeTwoLists(ListNode a, ListNode b) {
    ListNode dummy = new ListNode(0), tail = dummy;
    while (a != null && b != null) {
        if (a.val <= b.val) { tail.next = a; a = a.next; }
        else { tail.next = b; b = b.next; }
        tail = tail.next;
    }
    tail.next = (a != null) ? a : b;
    return dummy.next;
}""",
                "time": "O(n + m)",
                "space": "O(1)",
                "optimal": True,
            },
            {
                "name": "Recursive",
                "logic": "The smaller head keeps its place; merge the rest recursively and attach the result. Same time, but the call stack grows with the lists.",
                "code": """
ListNode mergeTwoLists(ListNode a, ListNode b) {
    if (a == null) return b;
    if (b == null) return a;
    if (a.val <= b.val) {
        a.next = mergeTwoLists(a.next, b);
        return a;
    }
    b.next = mergeTwoLists(a, b.next);
    return b;
}""",
                "time": "O(n + m)",
                "space": "O(n + m)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Remove Nth Node From End of List",
        "category": "Linked List",
        "aliases": ["remove nth node", "remove nth from end", "nth node from end", "delete nth node end"],
        "key_logic": "Two pointers kept n apart: when the front pointer hits the end, the rear pointer sits just before the node to remove.",
        "approaches": [
            {
                "name": "Two passes",
                "logic": "First pass counts the length; second pass walks to the node before the target and skips it. Simple, touches the list twice.",
                "code": """
ListNode removeNthFromEnd(ListNode head, int n) {
    int len = 0;
    for (ListNode p = head; p != null; p = p.next) len++;
    ListNode dummy = new ListNode(0, head), p = dummy;
    for (int i = 0; i < len - n; i++) p = p.next;
    p.next = p.next.next;
    return dummy.next;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "One pass, two pointers",
                "logic": "Move the front pointer n+1 steps ahead, then move both together. The gap guarantees the rear lands on the node before the target.",
                "code": """
ListNode removeNthFromEnd(ListNode head, int n) {
    ListNode dummy = new ListNode(0, head);
    ListNode front = dummy, rear = dummy;
    for (int i = 0; i <= n; i++) front = front.next;
    while (front != null) { front = front.next; rear = rear.next; }
    rear.next = rear.next.next;
    return dummy.next;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Valid Parentheses",
        "category": "Stack & Queue",
        "aliases": ["valid parentheses", "valid brackets", "balanced parentheses", "check parentheses"],
        "key_logic": "An opener must be closed by the matching closer, most recent first — exactly what a stack gives you.",
        "approaches": [
            {
                "name": "Stack",
                "logic": "Push openers; on a closer, the stack top must be its match. Anything left over, or a mismatch, means invalid.",
                "code": """
boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    Map<Character, Character> match = Map.of(')', '(', ']', '[', '}', '{');
    for (char c : s.toCharArray()) {
        if (match.containsKey(c)) {
            if (stack.isEmpty() || stack.pop() != match.get(c)) return false;
        } else {
            stack.push(c);
        }
    }
    return stack.isEmpty();
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": True,
            },
            {
                "name": "Counter (one bracket type only)",
                "logic": "Count +1 for '(' and −1 for ')'; never negative, end at zero. Constant space — but it only works when a single bracket type exists, so it fails mixed brackets.",
                "code": """
// ONLY for a single bracket type like "()()". Fails on "([)]".
boolean isValidSingleType(String s) {
    int depth = 0;
    for (char c : s.toCharArray()) {
        if (c == '(') depth++;
        else if (--depth < 0) return false;
    }
    return depth == 0;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Min Stack",
        "category": "Stack & Queue",
        "aliases": ["min stack", "minimum stack", "stack with getmin", "getmin stack"],
        "key_logic": "Carry the minimum along with the data, so getMin never has to rescan the stack.",
        "approaches": [
            {
                "name": "Rescan on getMin",
                "logic": "A plain stack; getMin scans everything. Push and pop stay fast, but the minimum query is slow — the opposite of what the problem asks.",
                "code": """
class MinStack {
    Deque<Integer> stack = new ArrayDeque<>();
    void push(int x) { stack.push(x); }
    void pop() { stack.pop(); }
    int top() { return stack.peek(); }
    int getMin() { // O(n) every call
        int min = Integer.MAX_VALUE;
        for (int x : stack) min = Math.min(min, x);
        return min;
    }
}""",
                "time": "O(n) per getMin",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Two stacks",
                "logic": "A second stack tracks the minimum at each height: push the new minimum alongside every push, pop both together.",
                "code": """
class MinStack {
    Deque<Integer> stack = new ArrayDeque<>();
    Deque<Integer> mins = new ArrayDeque<>();
    void push(int x) {
        stack.push(x);
        mins.push(mins.isEmpty() ? x : Math.min(x, mins.peek()));
    }
    void pop() { stack.pop(); mins.pop(); }
    int top() { return stack.peek(); }
    int getMin() { return mins.peek(); }
}""",
                "time": "O(1) per operation",
                "space": "O(n)",
                "optimal": True,
            },
            {
                "name": "Store pairs",
                "logic": "Each entry stores (value, minimum-so-far). One stack instead of two; same idea, slightly different packaging.",
                "code": """
class MinStack {
    record Entry(int value, int min) {}
    Deque<Entry> stack = new ArrayDeque<>();
    void push(int x) {
        int min = stack.isEmpty() ? x : Math.min(x, stack.peek().min());
        stack.push(new Entry(x, min));
    }
    void pop() { stack.pop(); }
    int top() { return stack.peek().value(); }
    int getMin() { return stack.peek().min(); }
}""",
                "time": "O(1) per operation",
                "space": "O(n)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Next Greater Element",
        "category": "Stack & Queue",
        "aliases": ["next greater element", "next greater", "next larger element", "nge"],
        "key_logic": "A decreasing stack holds elements still waiting for a greater one; each element is pushed and popped exactly once.",
        "approaches": [
            {
                "name": "Brute force",
                "logic": "For each element, scan right until a larger value appears. Simple, quadratic in the worst case.",
                "code": """
int[] nextGreater(int[] nums) {
    int[] ans = new int[nums.length];
    for (int i = 0; i < nums.length; i++) {
        ans[i] = -1;
        for (int j = i + 1; j < nums.length; j++)
            if (nums[j] > nums[i]) { ans[i] = nums[j]; break; }
    }
    return ans;
}""",
                "time": "O(n²)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Monotonic stack",
                "logic": "Scan once, keeping a decreasing stack of indices. A new element resolves every smaller element waiting on the stack, then joins it.",
                "code": """
int[] nextGreater(int[] nums) {
    int[] ans = new int[nums.length];
    Arrays.fill(ans, -1);
    Deque<Integer> stack = new ArrayDeque<>(); // indices, decreasing values
    for (int i = 0; i < nums.length; i++) {
        while (!stack.isEmpty() && nums[i] > nums[stack.peek()]) {
            ans[stack.pop()] = nums[i];
        }
        stack.push(i);
    }
    return ans;
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Binary Tree Traversals",
        "category": "Trees",
        "aliases": ["binary tree traversal", "tree traversal", "inorder", "preorder", "postorder", "dfs traversal tree", "traverse binary tree"],
        "key_logic": "DFS visits root-left-right in different orders; the order decides what the traversal is for — inorder of a BST gives sorted values, preorder rebuilds the tree.",
        "approaches": [
            {
                "name": "Recursive DFS",
                "logic": "The call stack does the work: visit in the order the traversal defines. The clearest code, and the standard interview answer.",
                "code": """
// Inorder: left, root, right. Swap the lines for pre/postorder.
void inorder(TreeNode root, List<Integer> out) {
    if (root == null) return;
    inorder(root.left, out);
    out.add(root.val);
    inorder(root.right, out);
}""",
                "time": "O(n)",
                "space": "O(h)",
                "optimal": True,
            },
            {
                "name": "Iterative with a stack",
                "logic": "Manage your own stack instead of recursion: push left children, visit, then go right. Same result, no call-stack depth limit.",
                "code": """
List<Integer> inorder(TreeNode root) {
    List<Integer> out = new ArrayList<>();
    Deque<TreeNode> stack = new ArrayDeque<>();
    while (root != null || !stack.isEmpty()) {
        while (root != null) { stack.push(root); root = root.left; }
        root = stack.pop();
        out.add(root.val);
        root = root.right;
    }
    return out;
}""",
                "time": "O(n)",
                "space": "O(h)",
                "optimal": False,
            },
            {
                "name": "Morris traversal",
                "logic": "Temporarily rewire the tree's empty right pointers to thread back up, then restore them. Constant space, but advanced and easy to get wrong.",
                "code": """
// Inorder, O(1) space. Threads the tree, then restores it.
List<Integer> inorder(TreeNode root) {
    List<Integer> out = new ArrayList<>();
    TreeNode curr = root;
    while (curr != null) {
        if (curr.left == null) { out.add(curr.val); curr = curr.right; }
        else {
            TreeNode pred = curr.left;
            while (pred.right != null && pred.right != curr) pred = pred.right;
            if (pred.right == null) { pred.right = curr; curr = curr.left; }
            else { pred.right = null; out.add(curr.val); curr = curr.right; }
        }
    }
    return out;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Maximum Depth of Binary Tree",
        "category": "Trees",
        "aliases": ["maximum depth binary tree", "max depth tree", "height of binary tree", "depth of tree"],
        "key_logic": "A tree's depth is 1 plus the deeper of its two subtrees. The recursion writes itself.",
        "approaches": [
            {
                "name": "Recursive DFS",
                "logic": "Depth of an empty tree is 0; otherwise 1 + max(depth of children). The cleanest solution by far.",
                "code": """
int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}""",
                "time": "O(n)",
                "space": "O(h)",
                "optimal": True,
            },
            {
                "name": "BFS level order",
                "logic": "Walk level by level with a queue and count the levels. The queue holds one full level at a time.",
                "code": """
int maxDepth(TreeNode root) {
    if (root == null) return 0;
    Queue<TreeNode> queue = new ArrayDeque<>(List.of(root));
    int depth = 0;
    while (!queue.isEmpty()) {
        depth++;
        for (int i = queue.size(); i > 0; i--) {
            TreeNode node = queue.remove();
            if (node.left != null) queue.add(node.left);
            if (node.right != null) queue.add(node.right);
        }
    }
    return depth;
}""",
                "time": "O(n)",
                "space": "O(w)",
                "optimal": False,
            },
            {
                "name": "Iterative DFS with a stack",
                "logic": "Track (node, depth) pairs on your own stack and keep the maximum depth seen. Recursion-free, same idea.",
                "code": """
int maxDepth(TreeNode root) {
    if (root == null) return 0;
    Deque<TreeNode> nodes = new ArrayDeque<>();
    Deque<Integer> depths = new ArrayDeque<>();
    nodes.push(root); depths.push(1);
    int best = 0;
    while (!nodes.isEmpty()) {
        TreeNode node = nodes.pop();
        int d = depths.pop();
        best = Math.max(best, d);
        if (node.left != null) { nodes.push(node.left); depths.push(d + 1); }
        if (node.right != null) { nodes.push(node.right); depths.push(d + 1); }
    }
    return best;
}""",
                "time": "O(n)",
                "space": "O(h)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Invert Binary Tree",
        "category": "Trees",
        "aliases": ["invert binary tree", "invert tree", "mirror tree", "flip binary tree"],
        "key_logic": "Swap every node's left and right children, then do the same for both subtrees. The mirror builds itself.",
        "approaches": [
            {
                "name": "Recursive swap",
                "logic": "Swap the children, then recurse on both. Three lines of real logic — the classic answer.",
                "code": """
TreeNode invertTree(TreeNode root) {
    if (root == null) return null;
    TreeNode tmp = root.left;
    root.left = invertTree(root.right);
    root.right = invertTree(tmp);
    return root;
}""",
                "time": "O(n)",
                "space": "O(h)",
                "optimal": True,
            },
            {
                "name": "Iterative with a queue",
                "logic": "BFS through the tree, swapping each node's children as you visit. Same result without recursion.",
                "code": """
TreeNode invertTree(TreeNode root) {
    if (root == null) return null;
    Queue<TreeNode> queue = new ArrayDeque<>(List.of(root));
    while (!queue.isEmpty()) {
        TreeNode node = queue.remove();
        TreeNode tmp = node.left;
        node.left = node.right;
        node.right = tmp;
        if (node.left != null) queue.add(node.left);
        if (node.right != null) queue.add(node.right);
    }
    return root;
}""",
                "time": "O(n)",
                "space": "O(w)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Validate Binary Search Tree",
        "category": "Trees",
        "aliases": ["validate bst", "validate binary search tree", "check bst", "is valid bst"],
        "key_logic": "Every node must sit inside a valid (min, max) range inherited from its ancestors — comparing with the parent alone is not enough.",
        "approaches": [
            {
                "name": "Brute force subtree checks",
                "logic": "For each node, verify its whole left subtree is smaller and right subtree larger by scanning both. Repeats the same scans at every level.",
                "code": """
boolean isValidBST(TreeNode root) {
    if (root == null) return true;
    return allSmaller(root.left, root.val)
        && allGreater(root.right, root.val)
        && isValidBST(root.left) && isValidBST(root.right);
}
boolean allSmaller(TreeNode node, int val) {
    if (node == null) return true;
    return node.val < val && allSmaller(node.left, val) && allSmaller(node.right, val);
}
boolean allGreater(TreeNode node, int val) {
    if (node == null) return true;
    return node.val > val && allGreater(node.left, val) && allGreater(node.right, val);
}""",
                "time": "O(n²)",
                "space": "O(h)",
                "optimal": False,
            },
            {
                "name": "Inorder + sorted check",
                "logic": "Inorder traversal of a BST must be strictly increasing. Walk it and check each value beats the previous one.",
                "code": """
boolean isValidBST(TreeNode root) {
    return inorder(root, new long[]{Long.MIN_VALUE});
}
boolean inorder(TreeNode node, long[] prev) {
    if (node == null) return true;
    if (!inorder(node.left, prev)) return false;
    if (node.val <= prev[0]) return false;
    prev[0] = node.val;
    return inorder(node.right, prev);
}""",
                "time": "O(n)",
                "space": "O(h)",
                "optimal": False,
            },
            {
                "name": "Range check (min, max)",
                "logic": "Carry the allowed range down: left children must stay below the parent, right children above it, tightened by every ancestor.",
                "code": """
boolean isValidBST(TreeNode root) {
    return check(root, Long.MIN_VALUE, Long.MAX_VALUE);
}
boolean check(TreeNode node, long lo, long hi) {
    if (node == null) return true;
    if (node.val <= lo || node.val >= hi) return false;
    return check(node.left, lo, node.val) && check(node.right, node.val, hi);
}""",
                "time": "O(n)",
                "space": "O(h)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Lowest Common Ancestor of a BST",
        "category": "Trees",
        "aliases": ["lowest common ancestor", "lca bst", "lca of bst", "lowest common ancestor bst"],
        "key_logic": "In a BST the split point is the answer: go left if both targets are smaller, right if both are larger — otherwise you are standing on the LCA.",
        "approaches": [
            {
                "name": "Path lists",
                "logic": "Record the root-to-target path for both nodes; the last common node on the two paths is the LCA. General, but stores both paths.",
                "code": """
TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    List<TreeNode> pathP = pathTo(root, p), pathQ = pathTo(root, q);
    TreeNode lca = root;
    for (int i = 0; i < Math.min(pathP.size(), pathQ.size()); i++) {
        if (pathP.get(i) == pathQ.get(i)) lca = pathP.get(i);
        else break;
    }
    return lca;
}
List<TreeNode> pathTo(TreeNode root, TreeNode target) {
    List<TreeNode> path = new ArrayList<>();
    while (root != target) {
        path.add(root);
        root = target.val < root.val ? root.left : root.right;
    }
    path.add(root);
    return path;
}""",
                "time": "O(h)",
                "space": "O(h)",
                "optimal": False,
            },
            {
                "name": "Iterative BST walk",
                "logic": "Walk down using the BST order: both targets smaller, go left; both larger, go right; split means current node is the LCA. No extra memory.",
                "code": """
TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    while (root != null) {
        if (p.val < root.val && q.val < root.val) root = root.left;
        else if (p.val > root.val && q.val > root.val) root = root.right;
        else return root;
    }
    return null;
}""",
                "time": "O(h)",
                "space": "O(1)",
                "optimal": True,
            },
            {
                "name": "Recursive BST walk",
                "logic": "Same split logic as the iterative walk, written recursively. The recursion depth is the tree height.",
                "code": """
TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (p.val < root.val && q.val < root.val)
        return lowestCommonAncestor(root.left, p, q);
    if (p.val > root.val && q.val > root.val)
        return lowestCommonAncestor(root.right, p, q);
    return root;
}""",
                "time": "O(h)",
                "space": "O(h)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Breadth-First Search (BFS)",
        "category": "Graphs",
        "aliases": ["bfs", "breadth first search", "breadth-first search", "level order traversal graph"],
        "key_logic": "A queue visits nodes level by level — the first time you reach a node is by the shortest path. That is why BFS finds shortest paths in unweighted graphs.",
        "approaches": [
            {
                "name": "Queue + visited set",
                "logic": "Push the start node, then repeatedly pop, visit, and push unvisited neighbours. The visited set stops revisits and infinite loops.",
                "code": """
void bfs(Map<Integer, List<Integer>> graph, int start) {
    Queue<Integer> queue = new ArrayDeque<>(List.of(start));
    Set<Integer> visited = new HashSet<>(Set.of(start));
    while (!queue.isEmpty()) {
        int node = queue.remove();
        // visit(node)
        for (int next : graph.getOrDefault(node, List.of()))
            if (visited.add(next)) queue.add(next);
    }
}""",
                "time": "O(V + E)",
                "space": "O(V)",
                "optimal": True,
            },
            {
                "name": "Level-by-level BFS",
                "logic": "Process the queue one level at a time (snapshot its size per level). Same traversal, but you know each node's distance from the start.",
                "code": """
List<List<Integer>> bfsLevels(Map<Integer, List<Integer>> graph, int start) {
    List<List<Integer>> levels = new ArrayList<>();
    Queue<Integer> queue = new ArrayDeque<>(List.of(start));
    Set<Integer> visited = new HashSet<>(Set.of(start));
    while (!queue.isEmpty()) {
        List<Integer> level = new ArrayList<>();
        for (int i = queue.size(); i > 0; i--) {
            int node = queue.remove();
            level.add(node);
            for (int next : graph.getOrDefault(node, List.of()))
                if (visited.add(next)) queue.add(next);
        }
        levels.add(level);
    }
    return levels;
}""",
                "time": "O(V + E)",
                "space": "O(V)",
                "optimal": False,
            },
            {
                "name": "BFS on a grid",
                "logic": "Same queue idea on a 2D grid: neighbours are the four directions, and visited cells are marked in place. The workhorse for shortest-path-on-grid problems.",
                "code": """
// Shortest distance from (0,0) in a grid; -1 means blocked.
int bfsGrid(int[][] grid) {
    int R = grid.length, C = grid[0].length;
    int[][] dist = new int[R][C];
    Queue<int[]> queue = new ArrayDeque<>(List.of(new int[]{0, 0}));
    grid[0][0] = -1;
    int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    while (!queue.isEmpty()) {
        int[] cell = queue.remove();
        for (int[] d : dirs) {
            int r = cell[0] + d[0], c = cell[1] + d[1];
            if (r >= 0 && r < R && c >= 0 && c < C && grid[r][c] != -1) {
                grid[r][c] = -1;
                dist[r][c] = dist[cell[0]][cell[1]] + 1;
                queue.add(new int[]{r, c});
            }
        }
    }
    return dist[R - 1][C - 1];
}""",
                "time": "O(R·C)",
                "space": "O(R·C)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Depth-First Search (DFS)",
        "category": "Graphs",
        "aliases": ["dfs", "depth first search", "depth-first search", "graph dfs"],
        "key_logic": "Go as deep as possible before backtracking. Recursion or an explicit stack — the stack, real or manual, is the whole technique.",
        "approaches": [
            {
                "name": "Recursive DFS",
                "logic": "Visit a node, mark it, recurse into each unvisited neighbour. The call stack remembers the path back. The standard form for most graph problems.",
                "code": """
void dfs(Map<Integer, List<Integer>> graph, int node, Set<Integer> visited) {
    visited.add(node);
    // visit(node)
    for (int next : graph.getOrDefault(node, List.of()))
        if (!visited.contains(next))
            dfs(graph, next, visited);
}""",
                "time": "O(V + E)",
                "space": "O(V)",
                "optimal": True,
            },
            {
                "name": "Iterative DFS with a stack",
                "logic": "Push neighbours on your own stack instead of recursing. Same visit order family, no recursion-depth limit — useful for very deep graphs.",
                "code": """
void dfs(Map<Integer, List<Integer>> graph, int start) {
    Deque<Integer> stack = new ArrayDeque<>(List.of(start));
    Set<Integer> visited = new HashSet<>(Set.of(start));
    while (!stack.isEmpty()) {
        int node = stack.pop();
        // visit(node)
        for (int next : graph.getOrDefault(node, List.of()))
            if (visited.add(next)) stack.push(next);
    }
}""",
                "time": "O(V + E)",
                "space": "O(V)",
                "optimal": False,
            },
            {
                "name": "DFS on a grid",
                "logic": "Flood-fill recursion on a grid: mark the cell, recurse in four directions. The core of island counting, area problems, and flood fill.",
                "code": """
void dfsGrid(char[][] grid, int r, int c) {
    if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length) return;
    if (grid[r][c] != '1') return;
    grid[r][c] = '0'; // mark visited in place
    dfsGrid(grid, r + 1, c);
    dfsGrid(grid, r - 1, c);
    dfsGrid(grid, r, c + 1);
    dfsGrid(grid, r, c - 1);
}""",
                "time": "O(R·C)",
                "space": "O(R·C)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Number of Islands",
        "category": "Graphs",
        "aliases": ["number of islands", "count islands", "islands problem", "count of islands"],
        "key_logic": "Each unvisited '1' starts a new island; flood-fill it so its land is never counted twice.",
        "approaches": [
            {
                "name": "DFS flood fill",
                "logic": "Scan the grid; on an unvisited '1', count one island and recursively sink the whole island to '0'. The most common interview answer.",
                "code": """
int numIslands(char[][] grid) {
    int islands = 0;
    for (int r = 0; r < grid.length; r++)
        for (int c = 0; c < grid[0].length; c++)
            if (grid[r][c] == '1') { islands++; sink(grid, r, c); }
    return islands;
}
void sink(char[][] grid, int r, int c) {
    if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length) return;
    if (grid[r][c] != '1') return;
    grid[r][c] = '0';
    sink(grid, r + 1, c); sink(grid, r - 1, c);
    sink(grid, r, c + 1); sink(grid, r, c - 1);
}""",
                "time": "O(R·C)",
                "space": "O(R·C) worst case",
                "optimal": True,
            },
            {
                "name": "BFS flood fill",
                "logic": "Same scan, but each island is sunk with a queue instead of recursion. No recursion depth risk on huge islands.",
                "code": """
int numIslands(char[][] grid) {
    int islands = 0;
    int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    for (int r = 0; r < grid.length; r++)
        for (int c = 0; c < grid[0].length; c++) {
            if (grid[r][c] != '1') continue;
            islands++;
            Queue<int[]> queue = new ArrayDeque<>(List.of(new int[]{r, c}));
            grid[r][c] = '0';
            while (!queue.isEmpty()) {
                int[] cell = queue.remove();
                for (int[] d : dirs) {
                    int nr = cell[0] + d[0], nc = cell[1] + d[1];
                    if (nr >= 0 && nr < grid.length && nc >= 0 && nc < grid[0].length
                            && grid[nr][nc] == '1') {
                        grid[nr][nc] = '0';
                        queue.add(new int[]{nr, nc});
                    }
                }
            }
        }
    return islands;
}""",
                "time": "O(R·C)",
                "space": "O(R·C) worst case",
                "optimal": False,
            },
            {
                "name": "Union-Find",
                "logic": "Union every land cell with its land neighbours, then count distinct roots. No flood fill at all — good when the grid changes over time.",
                "code": """
// Sketch: parent array over R*C cells; union right/down neighbours.
int numIslands(char[][] grid) {
    int R = grid.length, C = grid[0].length;
    int[] parent = new int[R * C];
    for (int i = 0; i < parent.length; i++) parent[i] = i;
    // union(r, c) with (r+1, c) and (r, c+1) when both are '1' ...
    Set<Integer> roots = new HashSet<>();
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            if (grid[r][c] == '1') roots.add(find(parent, r * C + c));
    return roots.size();
}
int find(int[] parent, int x) {
    if (parent[x] != x) parent[x] = find(parent, parent[x]);
    return parent[x];
}""",
                "time": "O(R·C·α)",
                "space": "O(R·C)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Climbing Stairs",
        "category": "Dynamic Programming",
        "aliases": ["climbing stairs", "climb stairs", "stairs problem", "ways to climb stairs"],
        "key_logic": "Ways to reach step n equal ways to n−1 plus ways to n−2 — the Fibonacci recurrence. The whole problem is not recomputing it.",
        "approaches": [
            {
                "name": "Plain recursion",
                "logic": "Directly code the recurrence. The same subproblems get solved exponentially many times — the classic DP motivation.",
                "code": """
int climbStairs(int n) {
    if (n <= 2) return n;
    return climbStairs(n - 1) + climbStairs(n - 2);
}""",
                "time": "O(2^n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Memoization",
                "logic": "Cache each answer the first time it is computed. Every subproblem is solved once; the recursion structure stays.",
                "code": """
int climbStairs(int n) {
    return solve(n, new HashMap<>());
}
int solve(int n, Map<Integer, Integer> memo) {
    if (n <= 2) return n;
    if (memo.containsKey(n)) return memo.get(n);
    int ans = solve(n - 1, memo) + solve(n - 2, memo);
    memo.put(n, ans);
    return ans;
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Two variables",
                "logic": "Only the last two answers matter, so keep two variables and roll forward. Same time as memoization, constant space.",
                "code": """
int climbStairs(int n) {
    if (n <= 2) return n;
    int prev2 = 1, prev1 = 2;
    for (int i = 3; i <= n; i++) {
        int cur = prev1 + prev2;
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "House Robber",
        "category": "Dynamic Programming",
        "aliases": ["house robber", "rob houses", "house robber problem", "maximum robbery"],
        "key_logic": "At each house, choose: rob it (plus the best up to two houses back) or skip it (keep the best up to the previous house).",
        "approaches": [
            {
                "name": "Plain recursion",
                "logic": "Try rob/skip at every house recursively. Exponential — the same suffixes are re-decided constantly.",
                "code": """
int rob(int[] nums) { return solve(nums, 0); }
int solve(int[] nums, int i) {
    if (i >= nums.length) return 0;
    return Math.max(nums[i] + solve(nums, i + 2), solve(nums, i + 1));
}""",
                "time": "O(2^n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "DP array",
                "logic": "dp[i] is the best loot considering houses up to i. Fill it left to right using the rob/skip choice.",
                "code": """
int rob(int[] nums) {
    if (nums.length == 1) return nums[0];
    int[] dp = new int[nums.length];
    dp[0] = nums[0];
    dp[1] = Math.max(nums[0], nums[1]);
    for (int i = 2; i < nums.length; i++)
        dp[i] = Math.max(dp[i - 1], dp[i - 2] + nums[i]);
    return dp[nums.length - 1];
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Two variables",
                "logic": "Only the previous two dp values are ever used, so two rolling variables replace the whole array.",
                "code": """
int rob(int[] nums) {
    int prev2 = 0, prev1 = 0;
    for (int n : nums) {
        int cur = Math.max(prev1, prev2 + n);
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Coin Change",
        "category": "Dynamic Programming",
        "aliases": ["coin change", "minimum coins", "fewest coins", "coin change problem"],
        "key_logic": "dp[amount] equals 1 plus the fewest coins for (amount − coin), tried over every coin. Build it from 0 up to the target.",
        "approaches": [
            {
                "name": "Plain recursion",
                "logic": "Try every coin as the first pick and recurse on the remainder. The same amounts are recomputed exponentially often.",
                "code": """
int coinChange(int[] coins, int amount) {
    if (amount == 0) return 0;
    if (amount < 0) return -1;
    int best = Integer.MAX_VALUE;
    for (int coin : coins) {
        int sub = coinChange(coins, amount - coin);
        if (sub >= 0) best = Math.min(best, sub + 1);
    }
    return best == Integer.MAX_VALUE ? -1 : best;
}""",
                "time": "Exponential",
                "space": "O(amount)",
                "optimal": False,
            },
            {
                "name": "Memoization (top-down)",
                "logic": "Same recursion, but each amount is solved once and cached. The recursion mirrors the problem statement directly.",
                "code": """
int coinChange(int[] coins, int amount) {
    return solve(coins, amount, new HashMap<>());
}
int solve(int[] coins, int amount, Map<Integer, Integer> memo) {
    if (amount == 0) return 0;
    if (amount < 0) return -1;
    if (memo.containsKey(amount)) return memo.get(amount);
    int best = Integer.MAX_VALUE;
    for (int coin : coins) {
        int sub = solve(coins, amount - coin, memo);
        if (sub >= 0) best = Math.min(best, sub + 1);
    }
    int ans = best == Integer.MAX_VALUE ? -1 : best;
    memo.put(amount, ans);
    return ans;
}""",
                "time": "O(amount·n)",
                "space": "O(amount)",
                "optimal": False,
            },
            {
                "name": "Bottom-up DP",
                "logic": "Fill dp[0..amount] in order; each entry tries every coin against an already-solved smaller amount. No recursion, no repeated work.",
                "code": """
int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1); // sentinel for "impossible"
    dp[0] = 0;
    for (int a = 1; a <= amount; a++)
        for (int coin : coins)
            if (coin <= a) dp[a] = Math.min(dp[a], dp[a - coin] + 1);
    return dp[amount] > amount ? -1 : dp[amount];
}""",
                "time": "O(amount·n)",
                "space": "O(amount)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Quick Sort",
        "category": "Sorting",
        "aliases": ["quick sort", "quicksort", "quick sort algorithm"],
        "key_logic": "Pick a pivot, partition so smaller elements go left and larger go right, then sort both sides. The partition scheme is the whole algorithm.",
        "approaches": [
            {
                "name": "Lomuto partition",
                "logic": "Use the last element as pivot; one pointer tracks the boundary of smaller elements. The easiest partition to write correctly.",
                "code": """
void quickSort(int[] a, int lo, int hi) {
    if (lo >= hi) return;
    int pivot = a[hi], i = lo;
    for (int j = lo; j < hi; j++)
        if (a[j] < pivot) swap(a, i++, j);
    swap(a, i, hi);
    quickSort(a, lo, i - 1);
    quickSort(a, i + 1, hi);
}
void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }""",
                "time": "O(n log n) average, O(n²) worst",
                "space": "O(log n)",
                "optimal": False,
            },
            {
                "name": "Hoare partition",
                "logic": "Two pointers move toward each other from both ends, swapping out-of-place pairs. Fewer swaps than Lomuto and the classic efficient form.",
                "code": """
void quickSort(int[] a, int lo, int hi) {
    if (lo >= hi) return;
    int pivot = a[lo], i = lo - 1, j = hi + 1;
    while (true) {
        do { i++; } while (a[i] < pivot);
        do { j--; } while (a[j] > pivot);
        if (i >= j) break;
        swap(a, i, j);
    }
    quickSort(a, lo, j);
    quickSort(a, j + 1, hi);
}
void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }""",
                "time": "O(n log n) average, O(n²) worst",
                "space": "O(log n)",
                "optimal": True,
            },
            {
                "name": "3-way partition (duplicates)",
                "logic": "Split into less-than, equal, and greater-than pivot groups, and only recurse on the outer two. With many duplicates this beats both schemes.",
                "code": """
void quickSort(int[] a, int lo, int hi) {
    if (lo >= hi) return;
    int pivot = a[lo], lt = lo, i = lo + 1, gt = hi;
    while (i <= gt) {
        if (a[i] < pivot) swap(a, lt++, i++);
        else if (a[i] > pivot) swap(a, i, gt--);
        else i++;
    }
    quickSort(a, lo, lt - 1);
    quickSort(a, gt + 1, hi);
}
void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }""",
                "time": "O(n log n) average, O(n) all-equal",
                "space": "O(log n)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Merge Sort",
        "category": "Sorting",
        "aliases": ["merge sort", "mergesort", "merge sort algorithm"],
        "key_logic": "Split the array in half until single elements, then merge the sorted halves back together. Always O(n log n) — no bad pivot case.",
        "approaches": [
            {
                "name": "Top-down recursive",
                "logic": "Recursively sort each half, then merge with a temporary array. The standard, stable, guaranteed-fast version.",
                "code": """
void mergeSort(int[] a, int lo, int hi) {
    if (hi - lo <= 1) return;
    int mid = (lo + hi) / 2;
    mergeSort(a, lo, mid);
    mergeSort(a, mid, hi);
    int[] tmp = new int[hi - lo];
    int i = lo, j = mid, k = 0;
    while (i < mid && j < hi)
        tmp[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
    while (i < mid) tmp[k++] = a[i++];
    while (j < hi) tmp[k++] = a[j++];
    System.arraycopy(tmp, 0, a, lo, tmp.length);
}""",
                "time": "O(n log n)",
                "space": "O(n)",
                "optimal": True,
            },
            {
                "name": "Bottom-up iterative",
                "logic": "Merge runs of size 1, then 2, then 4, doubling each pass. Same merges, no recursion at all.",
                "code": """
void mergeSort(int[] a) {
    int n = a.length;
    int[] tmp = new int[n];
    for (int width = 1; width < n; width *= 2)
        for (int lo = 0; lo < n; lo += 2 * width) {
            int mid = Math.min(lo + width, n);
            int hi = Math.min(lo + 2 * width, n);
            int i = lo, j = mid, k = lo;
            while (i < mid && j < hi)
                tmp[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
            while (i < mid) tmp[k++] = a[i++];
            while (j < hi) tmp[k++] = a[j++];
            System.arraycopy(tmp, lo, a, lo, hi - lo);
        }
}""",
                "time": "O(n log n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "In-place merge",
                "logic": "Merge without a temporary array by rotating/shifting elements. Constant space, but the merge step gets much slower and the code far trickier — rarely worth it.",
                "code": """
// Sketch: merge two sorted halves in place by insertion.
// Each out-of-order element is shifted right into place.
void mergeInPlace(int[] a, int lo, int mid, int hi) {
    int i = lo, j = mid;
    while (i < j && j < hi) {
        if (a[i] <= a[j]) { i++; continue; }
        int value = a[j];
        System.arraycopy(a, i, a, i + 1, j - i);
        a[i] = value;
        i++; j++;
    }
}""",
                "time": "O(n log n) with slow merges",
                "space": "O(1)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Kth Largest Element",
        "category": "Heap",
        "aliases": ["kth largest", "kth largest element", "k largest", "find kth largest"],
        "key_logic": "You only need the top k, not a full sort. A heap of size k keeps exactly the candidates that can still win.",
        "approaches": [
            {
                "name": "Sort",
                "logic": "Sort everything and pick index n−k. The simplest answer, and the baseline every other approach must beat.",
                "code": """
int findKthLargest(int[] nums, int k) {
    Arrays.sort(nums);
    return nums[nums.length - k];
}""",
                "time": "O(n log n)",
                "space": "O(log n)",
                "optimal": False,
            },
            {
                "name": "Min-heap of size k",
                "logic": "Keep a min-heap of the k largest seen so far; its top is the kth largest. Each element costs one heap operation of size k, not n.",
                "code": """
int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> heap = new PriorityQueue<>();
    for (int n : nums) {
        heap.add(n);
        if (heap.size() > k) heap.remove();
    }
    return heap.peek();
}""",
                "time": "O(n log k)",
                "space": "O(k)",
                "optimal": True,
            },
            {
                "name": "Quickselect",
                "logic": "Partition like quicksort, but recurse into only the side containing rank k. Average linear time; worst case quadratic without a good pivot.",
                "code": """
int findKthLargest(int[] nums, int k) {
    int target = nums.length - k, lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int p = partition(nums, lo, hi);
        if (p == target) return nums[p];
        if (p < target) lo = p + 1; else hi = p - 1;
    }
    return -1;
}
int partition(int[] a, int lo, int hi) {
    int pivot = a[hi], i = lo;
    for (int j = lo; j < hi; j++)
        if (a[j] < pivot) { int t = a[i]; a[i] = a[j]; a[j] = t; i++; }
    int t = a[i]; a[i] = a[hi]; a[hi] = t;
    return i;
}""",
                "time": "O(n) average, O(n²) worst",
                "space": "O(1)",
                "optimal": False,
            },
        ],
    },
    {
        "name": "Top K Frequent Elements",
        "category": "Heap",
        "aliases": ["top k frequent", "top k frequent elements", "k most frequent", "most frequent elements"],
        "key_logic": "Count frequencies first; the ranking step decides the complexity. Bucket sort by frequency is the linear-time trick.",
        "approaches": [
            {
                "name": "Sort by frequency",
                "logic": "Count with a map, sort the distinct elements by count, take the top k. Simple, dominated by the sort.",
                "code": """
int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int n : nums) freq.put(n, freq.getOrDefault(n, 0) + 1);
    List<Integer> keys = new ArrayList<>(freq.keySet());
    keys.sort((a, b) -> freq.get(b) - freq.get(a));
    int[] ans = new int[k];
    for (int i = 0; i < k; i++) ans[i] = keys.get(i);
    return ans;
}""",
                "time": "O(n log n)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Min-heap of size k",
                "logic": "Keep a heap of the k most frequent entries seen so far, ordered by count. Each distinct element costs one heap step of size k.",
                "code": """
int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int n : nums) freq.put(n, freq.getOrDefault(n, 0) + 1);
    PriorityQueue<Integer> heap =
        new PriorityQueue<>((a, b) -> freq.get(a) - freq.get(b));
    for (int key : freq.keySet()) {
        heap.add(key);
        if (heap.size() > k) heap.remove();
    }
    int[] ans = new int[k];
    for (int i = k - 1; i >= 0; i--) ans[i] = heap.remove();
    return ans;
}""",
                "time": "O(n log k)",
                "space": "O(n)",
                "optimal": False,
            },
            {
                "name": "Bucket sort by frequency",
                "logic": "Frequencies range from 1 to n, so bucket elements by their count and read the buckets from the top down. No comparisons at all.",
                "code": """
int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int n : nums) freq.put(n, freq.getOrDefault(n, 0) + 1);
    List<Integer>[] buckets = new List[nums.length + 1];
    for (int key : freq.keySet()) {
        int f = freq.get(key);
        if (buckets[f] == null) buckets[f] = new ArrayList<>();
        buckets[f].add(key);
    }
    int[] ans = new int[k];
    int w = 0;
    for (int f = buckets.length - 1; f >= 0 && w < k; f--)
        if (buckets[f] != null)
            for (int key : buckets[f]) ans[w++] = key;
    return ans;
}""",
                "time": "O(n)",
                "space": "O(n)",
                "optimal": True,
            },
        ],
    },
    {
        "name": "Prime Number Check",
        "category": "Math & Number Theory",
        "aliases": ["prime", "prime number", "prime check", "check prime", "is prime", "isprime", "primality", "sieve",
                    "prime number check", "abhaajya", "abhajya", "अभाज्य", "ప్రధాన సంఖ్య", "பகா எண்", "ಅವಿಭಾಜ್ಯ", "അഭാജ്യ"],
        "key_logic": "A prime has no divisors except 1 and itself. If n has a divisor larger than √n, it must also have one smaller than √n — so checking up to √n is enough.",
        "approaches": [
            {
                "name": "Trial division to n−1",
                "logic": "Try every divisor from 2 to n−1. The definition written as code — correct, and the slowest possible way.",
                "code": """
boolean isPrime(int n) {
    if (n <= 1) return false;
    for (int i = 2; i < n; i++)
        if (n % i == 0) return false;
    return true;
}""",
                "time": "O(n)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "Trial division to √n",
                "logic": "Only check divisors up to the square root: any factor above √n pairs with one below it, so nothing is missed. The single biggest speedup.",
                "code": """
boolean isPrime(int n) {
    if (n <= 1) return false;
    for (int i = 2; i * i <= n; i++)
        if (n % i == 0) return false;
    return true;
}""",
                "time": "O(√n)",
                "space": "O(1)",
                "optimal": False,
            },
            {
                "name": "6k ± 1 optimized",
                "logic": "Skip all multiples of 2 and 3: every prime above 3 sits next to a multiple of 6. Checks only 6k−1 and 6k+1 candidates — about 3× fewer divisions than plain √n trial division.",
                "code": """
boolean isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; i * i <= n; i += 6)
        if (n % i == 0 || n % (i + 2) == 0)
            return false;
    return true;
}""",
                "time": "O(√n)",
                "space": "O(1)",
                "optimal": True,
            },
            {
                "name": "Sieve of Eratosthenes",
                "logic": "A different job: find ALL primes up to n at once. Mark multiples of each prime as composite, starting from its square. Best when many numbers must be checked, wasteful for a single check.",
                "code": """
// All primes up to n — not a single-number check.
boolean[] sieve(int n) {
    boolean[] isPrime = new boolean[n + 1];
    Arrays.fill(isPrime, true);
    isPrime[0] = isPrime[1] = false;
    for (int i = 2; i * i <= n; i++)
        if (isPrime[i])
            for (int j = i * i; j <= n; j += i)
                isPrime[j] = false;
    return isPrime;
}""",
                "time": "O(n log log n)",
                "space": "O(n)",
                "optimal": False,
            },
        ],
    },
]

# --- Normalisation -------------------------------------------------------
# Trim the code blocks (they are written with a leading newline for
# readability) and merge the spoken-answer bank's keywords into each
# entry's aliases, so voice transcripts in any of the 10 languages match
# the same way they did before.
for _entry in ALGORITHMS:
    for _approach in _entry["approaches"]:
        _approach["code"] = _approach["code"].strip("\n")

_BANK_KEYWORDS = {}
for _bank in _BANK_ENTRIES:
    _BANK_KEYWORDS[_bank["topic"]] = list(_bank.get("keywords", []))
for _entry in ALGORITHMS:
    _seen = set(_entry["aliases"])
    for _kw in _BANK_KEYWORDS.get(_entry["name"], []):
        if _kw not in _seen:
            _entry["aliases"].append(_kw)
            _seen.add(_kw)


# --- Matching ------------------------------------------------------------

_STOPWORDS = {"a", "an", "the", "how", "what", "is", "to", "of", "in", "for", "do", "does", "explain", "tell", "me", "about"}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", (text or "").lower())).strip()


def _clean_tokens(text: str) -> list:
    return [t for t in _normalize(text).split() if t]


def _score_algorithm(entry: dict, raw: str, norm: str) -> float:
    # Alias phrase hits dominate; token overlap + fuzzy name similarity
    # rescue misheard / mistyped questions. Mirrors answers._score_entry.
    raw_low = (raw or "").lower()
    best_kw = 0.0
    for kw in entry["aliases"]:
        k = kw.lower()
        if k in norm or k in raw_low:
            best_kw = max(best_kw, 12.0 + len(k) / 4.0)
        else:
            kw_tokens = _clean_tokens(k)
            if kw_tokens and all(t in norm or t in raw_low for t in kw_tokens):
                best_kw = max(best_kw, 6.0)
    name_tokens = [t for t in _clean_tokens(entry["name"]) if t not in _STOPWORDS and len(t) > 2]
    query_tokens = set(_clean_tokens(norm)) | set(_clean_tokens(raw_low))
    overlap = sum(1 for t in name_tokens if t in query_tokens)
    fuzzy = 0.0
    if overlap:
        ratio = difflib.SequenceMatcher(None, " ".join(_clean_tokens(norm)), entry["name"].lower()).ratio()
        if ratio >= 0.55:
            fuzzy = ratio * 6.0
    return best_kw + min(overlap, 3) * 3.0 + fuzzy


_MATCH_THRESHOLD = 10.0


def find_algorithm(question: str) -> dict | None:
    """Best-matching algorithm entry for a question, or None."""
    norm = _normalize(question)
    scored = sorted(
        ((_score_algorithm(entry, question, norm), entry) for entry in ALGORITHMS),
        key=lambda pair: pair[0],
        reverse=True,
    )
    best_score, best_entry = scored[0] if scored else (0.0, None)
    if best_entry is not None and best_score >= _MATCH_THRESHOLD:
        return best_entry
    return None


def suggest_algorithms(query: str, limit: int = 6) -> list[dict]:
    """Top algorithm matches for live search suggestions.

    Prefix matches count too (typing "bin" should already suggest Binary
    Search), and an empty or matchless query falls back to popular picks
    so the box never looks dead.
    """
    popular = ["Prime Number Check", "Two Sum", "Binary Search", "Quick Sort", "Reverse Linked List", "Breadth-First Search (BFS)"]
    by_name = {e["name"]: e for e in ALGORITHMS}
    norm = _normalize(query)
    if not norm:
        return [{"name": n, "category": by_name[n]["category"]} for n in popular[:limit] if n in by_name]
    query_tokens = _clean_tokens(norm)
    scored = []
    for entry in ALGORITHMS:
        score = _score_algorithm(entry, query, norm)
        if len(norm) >= 2:
            haystacks = [entry["name"].lower()] + [a.lower() for a in entry["aliases"]]
            for hay in haystacks:
                for tok in hay.split():
                    if any(tok.startswith(q) for q in query_tokens if len(q) >= 2):
                        score += 4.0
                        break
        scored.append((score, entry))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    out = []
    for score, entry in scored:
        if score <= 0:
            continue
        out.append({"name": entry["name"], "category": entry["category"]})
        if len(out) >= limit:
            break
    if not out:
        return [{"name": n, "category": by_name[n]["category"]} for n in popular[:limit] if n in by_name]
    return out


def optimal_approach(entry: dict) -> dict | None:
    """The approach flagged optimal, if any."""
    for approach in entry["approaches"]:
        if approach.get("optimal"):
            return approach
    return None
