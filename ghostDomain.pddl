(define (domain ghost)
(:requirements :typing)
(:types node)
;; Define the facts in the problem
;; "?" denotes a variable, "-" a type
(:predicates (at ?pos - node)                   ;; ghost position
             (connected ?start ?end - node)     ;; adjacent nodes
             (pacmanAt ?pos - node)             ;; pacman positions
             (superPacman))                     ;; if pacman ate a capsule

;; the ghost can move to any position if it is adjacent to the current position
;; and isn't scared. position is updated. pacman is eaten.

(:action move 
            :parameters (?start - node ?end - node)
            :precondition (and (at ?start) 
                               (connected ?start ?end)
                               (not (superPacman)))
            :effect (and (not (at ?start))
                              (at ?end)
                              (not (pacmanAt ?end))))

;; the ghost can move to a position if it is adjacent to the current position
;; and pacman isn't at the adjacent position when pacman is scared. position is 
;; updated.

(:action scaredmove
            :parameters (?start - node ?end - node)
            :precondition (and (at ?start)
                               (connected ?start ?end)
                               (superPacman)
                               (not (pacmanAt ?end)))
            :effect (and (not (at ?start))
                              (not (at ?end)))))