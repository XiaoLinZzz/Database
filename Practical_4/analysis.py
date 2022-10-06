data_file = "Practical_4/movies.nt"
language_tag = "@en-US"
line_ending = " ."
query_person_name = "\"Guy Ritchie\""

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
    set_spo = set()
    n_guy_jobs = 0
    dict = {}
    # open file and read it line by line
    # assume utf8 encoding, ignore non-parseable characters
    with open(data_file, encoding="utf8", errors="ignore") as f:
        for line in f:
            # get subject, predicate and object
            s, p, o = _parse_line(line)
            set_spo.add((s, p, o))
            
            if o == uri_person and p == predicate_has_type:
                if s not in dict:
                    dict[s] = 1
                else:
                    dict[s] += 1
                    
            if s == query_person_name:
                if p not in dict:
                    dict[p] = 1
                else:
                    dict[p] += 1
                    
            if p == predicate_has_actor:
                if o not in dict:
                    dict[o] = 1
                else:
                    dict[o] += 1
                    

    n_triples = len(set_spo)
    n_people = len(dict)
        
    # return set_spo
                
                
            
    ###########################################################
    # ... your code here ...
    # you can add functions and variables as needed;
    # however, do NOT remove or modify existing code;
    # _compute_stats() must return four values as described;
    # you can add print statements if you like, but only the
    # last four printed lines will be assessed;
    ###########################################################
    
    
    
    ###########################################################
    # n_triples -- number of distinct triples
    # n_people -- number of distinct people mentioned in ANY role
    #             (e.g., actor, director, producer, etc.)
    # n_top_actors -- number of people appeared as ACTORS in
    #                 M movies, where M is the maximum number
    #                 of movies any person appeared in as an actor
    # n_guy_jobs -- number of distinct jobs that "Guy Ritchie" had
    #               across different movies (e.g., he could be a 
    #               director in one movie, producer in another, etc.)
    ###########################################################
    
    
    # return s, p, o
    return n_triples, n_people, n_top_actors, n_guy_jobs

    
if __name__ == "__main__":
    n_triples, n_people, n_top_actors, n_guy_jobs = _compute_stats()
    print()
    print(f"{n_triples:,} (n_triples)")
    print(f"{n_people:,} (n_people)")
    print(f"{n_top_actors} (n_top_actors)")
    print(f"{n_guy_jobs} (n_guy_jobs)")
    
    # s = _compute_stats()
    # print(s)