from helpers import memoize
from helpers import make_verbose
from helpers import pop_from_str
from helpers import normalize_string
from concurrent.futures import ThreadPoolExecutor
import spotipy


class spotify_playlist_maker(object):
    track_name_to_artist_lookup = {}
    spotify_obj = spotipy.Spotify()
    original_input_str = ''

    def __init__(self, command_line_input):
        self.original_input_str = command_line_input
        pass

    @memoize
    def search_spotify(self, track_name, spotify_obj):
        '''
        api call to spotify for it's track name
        '''
        return spotify_obj.search(q='track:' + track_name, type='track')

    def find_n_grams(self, input_str, n):
        '''
        I: a string, n for number of ngrams eg unigram:1, bigrams:2,..., ngrams:n 
        O: list of all ngrams in string
        '''
        target_list = input_str.split()
        ngrams = [target_list[i:i + n] for i in range(len(target_list) - n + 1)]
        return [' '.join(ngram) for ngram in ngrams]

    def query_all_possibilities_parallelized(self, input_str, max_workers=50):
        '''
        I: a string which is later split by word count starting with the largest
        O: 
        '''
        output = []
        with ThreadPoolExecutor(max_workers) as executor:
            for n in range(len(input_str.split()))[::-1]: #change to xrange
                #maps the function to the the distributable task_list 
                future = executor.submit(self.api_call_func, (input_str, n))
                output.append(future)
        
        #unpacks the result 
        lis = map(lambda x: x.result(), output)
        #unpacking
        return [item for sublist in lis for item in sublist if item]         

    def api_call_func(self, input_str_and_n_tuple):
        '''
        I: ('input string phrase', 2) 2 pertains the number of grams to search for 
        O: ngrams that are valid tracknames on spotify with corresponding length weight
            e.g. ('some ngram', 2)
        '''
        output = []
        input_str, n = input_str_and_n_tuple
        
        #try using a persistent object
        spotify_obj = spotipy.Spotify()
        ngram_set = self.find_n_grams(input_str, n + 1) 
        for ngram in ngram_set:
            results = self.search_spotify(ngram, spotify_obj)
            if results: 
                validated_results = self.search_through_results(ngram, results)
                if validated_results: 
                    output.append((ngram, n + 1))
                    #it just picks the first song that matches the target n_gram
                    self.track_name_to_artist_lookup[ngram] = validated_results[0]
        return output

    def search_through_results(self, target_n_gram, results_dict):
        stor = []
        normalized_target_n_gram = normalize_string(target_n_gram)
        for item in results_dict['tracks']['items']:
            normalized_track_name = normalize_string(item['name'])
            #filter
            if normalized_track_name == normalized_target_n_gram:
                stor.append(item['artists'][0]['name'])
        return stor

    def find_optimal_arrangement(self, loop_lis, input_str):
        output = []
        while loop_lis:
            # double check this line
            remaining_str = input_str
            bag = []
            for tup in loop_lis:
                remaining_str_len_before_pop = len(remaining_str)
                remaining_str = pop_from_str(remaining_str, tup[0])
                if remaining_str_len_before_pop > len(remaining_str): 
                    bag.append(tup[0])
            output.append((remaining_str.strip(), bag))
            loop_lis = loop_lis[1:]
        return sorted(output, key=lambda x: len(x[0]))

    # this avoids unnecessary api calls and saves time for algo optimization
    @memoize 
    # a decorator used for effective debugging seeing which calls are being made
    @make_verbose 
    def str_to_playlist(self, input_str): 
        all_valid_track_names = self.query_all_possibilities_parallelized(input_str)
        sorted_bag = self.find_optimal_arrangement(all_valid_track_names, input_str)        
        if sorted_bag: return self.format_output(sorted_bag)
        return None
    
    def format_output(self, sorted_bag):
        output_to_display = []
        for track_name in sorted_bag[0][1]:
            playlist_str = '"' + track_name + '"' + ' by ' + self.track_name_to_artist_lookup[track_name]
            output_to_display.append(playlist_str)
        return output_to_display

    def make_playlist(self, input_str=None):
        if not input_str: input_str = self.original_input_str
        return self.loop_through_sentence_by_sentence(input_str)

    def loop_through_sentence_by_sentence(self, input_str):
        output = []
        for phrase in input_str.split('\n'):
            results = self.str_to_playlist(phrase.strip())
            if results: output.append(results)
            else: continue
        return output