# def wordBreak( s, dict):
#     segmented = [True]
    
#     for i in range (0, len(s)):
#         segmented.append(False)
        
#         for j in range(i,-1,-1):
#             if segmented[j] and s[j:i + 1] in dict:
#                 segmented[i + 1] = True
#                 break

#     return segmented[len(s)]


def wordBreak(s, wordDict):
    n = len(s)
    is_breakable = [False] * (n + 1)
    # why is the first one set to true
    is_breakable[0] = True

    for i in xrange(1, n + 1):
        for j in xrange(0, i):
            print is_breakable[j],  s[j:i]
            if is_breakable[j] and s[j:i] in wordDict:
                is_breakable[i] = True
                break

    return is_breakable[n]

if __name__ == '__main__':

	s = "this is a sentence"

	dict = ["sentence", "this", "is"]
	print wordBreak(s.split(), dict)