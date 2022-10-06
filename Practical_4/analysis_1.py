data_file = "/Users/Uni Course/Database/Practical_4/movies.nt"
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
    # print(line)

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

    # print([s, p, o])
    return s, p, o


def _compute_stats():
    # ... you can add variables here ...
    spo_set = set()
    actor_movie = {}
    n_top_actors = 0
    query_person_node = ""
    query_person_jobs_set = set()
    people_set = set()
    # open file and read it line by line
    # assume utf8 encoding, ignore non-parseable characters
    with open(data_file, encoding="utf8", errors="ignore") as f:
        for line in f:
            # get subject, predicate and object
            s, p, o = _parse_line(line)
            spo_set.add(s + p + o)
            # if the object is a person
            if o == uri_person and p == predicate_has_type:
                people_set.add(s)
            # if the predicate is hasactor
            if p == predicate_has_actor:
                # if not have a set of current actor
                if o not in actor_movie:
                    actor_movie[o] = set()
                # add movie to current actor
                actor_movie[o].add(s)
            if o == query_person_name:
                query_person_node = s
        if query_person_node != "":
            with open(data_file, encoding="utf8", errors="ignore") as f:
                for line in f:
                    s, p, o = _parse_line(line)
                    if o == query_person_node and p.startswith(predicate_prefix):
                        tempjob = p.lstrip(predicate_prefix)
                        query_person_jobs_set.add(tempjob)
    n_triples = len(spo_set)
    n_people = len(people_set)

    maxcountmovie = 0
    for key, vaule in actor_movie.items():
        if len(vaule) > maxcountmovie:
            maxcountmovie = len(vaule)
    for key, vaule in actor_movie.items():
        if len(vaule) == maxcountmovie:
            n_top_actors += 1
    n_guy_jobs = len(query_person_jobs_set)

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

    return n_triples, n_people, n_top_actors, n_guy_jobs


if __name__ == "__main__":
    n_triples, n_people, n_top_actors, n_guy_jobs = _compute_stats()
    print()
    print(f"{n_triples:,} (n_triples)")
    print(f"{n_people:,} (n_people)")
    print(f"{n_top_actors} (n_top_actors)")
    print(f"{n_guy_jobs} (n_guy_jobs)")
