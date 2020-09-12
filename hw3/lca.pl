ancestor(A, B) :- parent(A, B).
ancestor(A, B) :- 
    parent(X, B), 
    ancestor(A, X).

lca(A, B, X) :- 
    ancestor(X, A), 
    ancestor(X, B).

add_rule(Predicate, X, Y) :-
    Fact =.. [Predicate, X, Y],
    assertz(Fact).

build_graph() :-
    read_line_to_string(user_input, S),
    split_string(S, " ", "", L),
    nth0(0, L, X), atom_string(X, A),
    nth0(1, L, Y), atom_string(Y, B),
    add_rule(parent, A, B).

init_rules() :-
    read_line_to_string(user_input, S),
    atom_number(S, NODES),
    foreach(between(2,NODES,_), build_graph()).

print_lca() :-
    read_line_to_string(user_input, S),
    split_string(S, " ", "", L),
    nth0(0, L, X), atom_string(X, A),
    nth0(1, L, Y), atom_string(Y, B),
    lca(A,B,LCA),
    format("~w~n", LCA),
    at_end_of_stream(user_input) ; true.

calc_input() :-
    read_line_to_string(user_input, S),
    atom_number(S, INPUTS),
    foreach(between(1,INPUTS,_), print_lca()).

main() :-
    prompt(_,''),
    init_rules(),
    calc_input(),
    halt.

:- initialization(main).
