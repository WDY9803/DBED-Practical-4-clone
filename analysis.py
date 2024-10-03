data_file = "movies.nt"
language_tag = "@en-US"
line_ending = " ."

predicate_has_type = "<http://adelaide.edu.au/dbed/hasType>"
predicate_has_name = "<http://adelaide.edu.au/dbed/hasName>"
predicate_has_actor = "<http://adelaide.edu.au/dbed/hasActor>"
uri_person = "<http://adelaide.edu.au/dbed/Person>"
predicate_prefix = "<http://adelaide.edu.au/dbed/has"


def _is_uri(some_text):
    # simple text without regular expressions
    if some_text.find(' ') >= 0:
        return False
    return some_text.startswith("<") and some_text.endswith(">")

def _is_blank_node(some_text):
    # simple text without regular expressions
    if some_text.find(' ') >= 0:
        return False
    return some_text.startswith("_:")

def _is_literal(some_text):
    return some_text.startswith("\"") and some_text.endswith("\"")
    
def _parse_line(line):
    # this could be done using regex
    
    # for each line, remove newline character(s)
    line = line.strip()
    #print(line)
    
    # throw an error if line doesn't end as required by file format
    assert line.endswith(line_ending), line
    # remove the ending part
    line = line[:-len(line_ending)]
    
    # find subject
    i = line.find(" ")
    # throw an error, if no whitespace
    assert i >= 0, line
    # split string into subject and the rest
    s = line[:i]
    line = line[(i + 1):]
    # throw an error if subject is neither a URI nor a blank node
    assert _is_uri(s) or _is_blank_node(s), s

    # find predicate
    i = line.find(" ")
    # throw an error, if no whitespace
    assert i >= 0, line
    # split string into predicate and the rest
    p = line[:i]
    line = line[(i + 1):]
    # throw an error if predicate is not a URI
    assert _is_uri(p), str(p)
    
    # object is everything else
    o = line
    
    # remove language tag if needed
    if o.endswith(language_tag):
        o = o[:-len(language_tag)]

    # object must be a URI, blank node, or string literal
    # throw an error if it's not
    assert _is_uri(o) or _is_blank_node(o) or _is_literal(o), o
    
    #print([s, p, o])
    return s, p, o

def _compute_stats():
    # ... you can add variables here ...
    set_triples = set() #set for unique n_tripes
    people_set = set() #set for distinct people in role
    actors_set = set() #set for all distinct actors\
    
    actors_dict = {} #dict for actors and num of movies that they have appeared in
    weights_dict = {} #dict for actors and their weights to cast order

    #initialise
    n_tripes = 0
    max_m = 0
    n_top_actors = 0
    cast_order = 1
    n_highweight_actor = 0

    movie = "" #name for current movie
    s_name = "" #name for highweight actor

    
    # open file and read it line by line
    # assume utf8 encoding, ignore non-parseable characters
    with open(data_file, encoding="utf8", errors="ignore") as f:
        for line in f:
            # get subject, predicate and object
            s, p, o = _parse_line(line)
            
    ###########################################################
    # ... your code here ...
    # you can add functions and variables as needed;
    # however, do NOT remove or modify existing code;
    # _compute_stats() must return four values as described;
    # you can add print statements if you like, but only the
    # last four printed lines will be assessed;
    ###########################################################
    
    #n_triples:
            set_triples.add((s,p,o))
            n_triples = len(set_triples)
    #n_triples += 1 #each line represent a n_triple

    #n_people:
            if _is_uri(o) == True and o == uri_person: #check the role
                people_set.add(s)
            n_people = len(people_set)

    #n_top_actors:
            if _is_uri(p) == True and p == predicate_has_actor: #check uif they are actor
                actors_set.add(o)
    for x in actors_set:
        actors_dict[x] = 0 #dict for actors and movies appeared
        weights_dict[x] = 0 #weights for actors to calculate n_highweight_actor
    with open(data_file, encoding="utf8", errors="ignore") as f:
        for line in f:
            s, p, o = _parse_line(line)
            if _is_uri(p) == True and p == predicate_has_actor:
                actors_dict[o] += 1
                if actors_dict[o] > max_m:
                    max_m = actors_dict[o]
    for x in actors_dict.values():
        if x == max_m:
            n_top_actors += 1
            
    #n_highweight_actor:
    with open(data_file, encoding="utf8", errors="ignore") as f:
        for line in f:
            s, p, o = _parse_line(line)
            if _is_uri(p) == True and p == predicate_has_actor:
                if s != movie:
                    movie = s
                    cast_order = 1
                weights_dict[o] += (1/cast_order)
                cast_order += 1

    for x in weights_dict:
        if weights_dict[x] > n_highweight_actor:
            n_highweight_actor = weights_dict[x]
            highweight_id = x

    #s_name:
    with open(data_file, encoding="utf8", errors="ignore") as f:
        for line in f:
            s, p, o = _parse_line(line)
            if _is_uri(p) == True and p == predicate_has_name and s == highweight_id:
                s_name_temp = o
                s_name = s_name_temp.replace('"','')
    
    ###########################################################
    # n_triples -- number of distinct triples
    # n_people -- number of distinct people mentioned in ANY role
    #             (e.g., actor, director, producer, etc.)
    # n_top_actors -- number of people appeared as ACTORS in
    #                 M movies, where M is the maximum number
    #                 of movies any person appeared in as an actor
    # n_highweight_actor -- the 'weight' of an actor is calculated by 
    #               dividing each 'appearance' by their place in 
    #               the cast list. If we add up all of these, we
    #               get the cumulative weight of the actor. The 
    #               'highweight' is the largest cumulative weight.
    # s_name -- the name of the highweight actor
    ###########################################################
    
    return n_triples, n_people, n_top_actors, n_highweight_actor, s_name

# DO NOT CHANGE THE FINAL OUTPUT FORMATTING BELOW THIS LINE
if __name__ == "__main__":
    n_triples, n_people, n_top_actors, n_highweight_actor, s_name = _compute_stats()
    print()
    print(f"{n_triples:,} (n_triples)")  #36,769 (n_triples)
    print(f"{n_people:,} (n_people)") #11,135 (n_people)
    print(f"{n_top_actors} (n_top_actors)") #12 (n_top_actors)
    print(f"{n_highweight_actor} (n_highweight_actor)") #3.5 (n_highweight_actor)
    print(f"{s_name} (s_name)") #Tom Hardy (s_name)




