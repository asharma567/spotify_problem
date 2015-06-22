'''
Spotify take home for product analyst role
'''
import sys
import spotipy
import string 

PUNC_SET = set(string.punctuation)

def normalize_string(target_str):
    removed_punc_str = ''.join([char for char in target_str if char not in PUNC_SET])
    return removed_punc_str.lower()

def pop_from_str(in_str, phrase_str):
    return in_str.replace(phrase_str, '').replace('  ', ' ')

def find_n_grams(input_str, n):
    target_list = input_str.split()
    ngrams = [target_list[i:i + n] for i in range(len(target_list) - n + 1)]
    return [' '.join(ngram) for ngram in ngrams]

def search_spotify(track_name, spotify_obj):
    return spotify_obj.search(q='track:' + track_name, type='track')

def query_all_possibilities(input_str):
    output = []
    spotify = spotipy.Spotify()
    for n in range(len(input_str.split()))[::-1]:
        ngram_set = find_n_grams(input_str, n + 1) 
        for ngram in ngram_set:
            results = search_spotify(ngram, spotify)
            if results: 
                validated_results = search_through_results(ngram, results)
                if validated_results: 
                    output.append((ngram, n + 1))
    return output

def search_through_results(target_n_gram, results_dict):
    
    #normally I'd write this in one line
    stor = []
    normalized_target_n_gram = normalize_string(target_n_gram)

    for item in results_dict['tracks']['items']:
        
        #write a normalize function
        normalized_track_name = normalize_string(item['name'])
        
        #filter
        if normalized_track_name == normalized_target_n_gram:
            
            #need to fix tolower
            stor.append(str(item['name'] + ' by ' + item['artists'][0]['name']))
            
    return stor

def find_optimal(loop_lis, original_input_str):
    output = []
    while loop_lis:
        remaining_str = original_input_str
        bag = []
        for tup in loop_lis:
            remaining_str_len_before_pop = len(remaining_str)
            remaining_str = pop_from_str(remaining_str, tup[0])
            if remaining_str_len_before_pop > len(remaining_str): 
                bag.append(tup[0])
        output.append((remaining_str.strip(), bag))
        loop_lis = loop_lis[1:]

    return sorted(output, key=lambda x: len(x[0]))

def main(command_line_input):
   all_possible_track_names = query_all_possibilities(command_line_input)
   sorted_bag = find_optimal(all_possible_track_names, command_line_input)
   print '\n'.join(sorted_bag[0][1])


if __name__ == '__main__':
    # command_line_input = sys.argv[1]
    command_line_input = "if i can't let it go out of my mind"
    main(command_line_input)