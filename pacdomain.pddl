(define (domain pacman)

    (:requirements
        :strips
    )

    (:predicates
    (at ?x ?y) ;co-ordinates of pacman's position
    (dotat ?d ?x ?y) ;dot co-ordinates
    (powerpillat ?p ?x ?y) ;power pill co-ordinates
    (eaten ?d) ;whether or not a dot has been eaten
    (powerup) ;whether or not pacman is powered up from a power pill
    (inc ?x1 ?x2) ;the change in the x-coordinate
    (dec ?y1 ?y2) ;the change in the y-coordinate
    (wall ?x ?y) ;wall co-ordinates
    (ghost ?x ?y) ;ghost co-ordinates
    )

    ;can only move in a certain direction if there are no walls or ghosts, and if the x or y co-ordinate for the next
    ;position matches the direction moved. power moves mean the pacman is powered up and can ignore the rule about ghosts.
    
    (:action move-right
        :parameters (?x1 ?x2 ?y)
        :precondition (and (at ?x1 ?y) (not (wall ?x2 ?y)) (not (ghost ?x2 ?y)) (inc ?x1 ?x2))
        :effect (and (at ?x2 ?y) (not (at ?x1 ?y)))
    )
    
    (:action move-right-power
        :parameters (?x1 ?x2 ?y ?p)
        :precondition (and (at ?x1 ?y) (powerup) (not (wall ?x2 ?y)) (inc ?x1 ?x2))
        :effect (and (at ?x2 ?y) (not (at ?x1 ?y)))
    )
    
    (:action move-left
        :parameters (?x1 ?x2 ?y)
        :precondition (and (at ?x1 ?y) (not (wall ?x2 ?y)) (not (ghost ?x2 ?y)) (dec ?x1 ?x2))
        :effect (and (at ?x2 ?y) (not (at ?x1 ?y)))
    )
    
    (:action move-left-power
        :parameters (?x1 ?x2 ?y)
        :precondition (and (at ?x1 ?y) (not (wall ?x2 ?y)) (powerup) (dec ?x1 ?x2))
        :effect (and (at ?x2 ?y) (not (at ?x1 ?y)))
    )
    
    (:action move-up
        :parameters (?x ?y1 ?y2)
        :precondition (and (at ?x ?y1) (not (wall ?x ?y2)) (not (ghost ?x ?y2)) (inc ?y1 ?y2))
        :effect (and (at ?x ?y2) (not (at ?x ?y1)))
    )
    
    (:action move-up-power
        :parameters (?x ?y1 ?y2)
        :precondition (and (at ?x ?y1) (not (wall ?x ?y2)) (powerup) (inc ?y1 ?y2))
        :effect (and (at ?x ?y2) (not (at ?x ?y1)))
    )
    
    (:action move-down
        :parameters (?x ?y1 ?y2)
        :precondition (and (at ?x ?y1) (not (wall ?x ?y2)) (not (ghost ?x ?y2)) (dec ?y1 ?y2))
        :effect (and (at ?x ?y2) (not (at ?x ?y1)))
    )
    
    (:action move-down-power
        :parameters (?x ?y1 ?y2)
        :precondition (and (at ?x ?y1) (not (wall ?x ?y2)) (powerup) (dec ?y1 ?y2))
        :effect (and (at ?x ?y2) (not (at ?x ?y1)))
    )
    
    (:action eat
        :parameters (?x ?y ?d)
        :precondition (and (dotat ?d ?x ?y) (at ?x ?y))
        :effect (and (eaten ?d) (not (dotat ?d ?x ?y)))
    )
    
    (:action eat-power
        :parameters (?x ?y ?p)
        :precondition (and (powerpillat ?p ?x ?y) (at ?x ?y))
        :effect (and (eaten ?p) (not (powerpillat ?p ?x ?y)) (powerup))
    )
    )