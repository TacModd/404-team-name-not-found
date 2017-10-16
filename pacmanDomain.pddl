(define (domain pacman)
(:requirements :typing)
(:types node)
;; Define the facts in the problem
;; "?" denotes a variable, "-" a type
(:predicates (at ?pos - node)                   ;; pacman position
             (connected ?start ?end - node)     ;; adjacent nodes
             (ghostAt ?pos - node)              ;; ghost positions
             (foodAt ?pos - node)               ;; food positions
             (capsuleAt ?pos - node)            ;; capsule positions
             (superPacman))                      ;; if a capsule has been eaten

;; pacman can move to a position if it is next to the current position
;; and there is no ghost at the adjacent position. position is updated. food is 
;; eaten. if there is a capsule, it is eaten and pacman becomes superpacman 
;; (ghosts scared)
             
(:action move
            :parameters (?start - node ?end - node)
            :precondition (and (at ?start) 
                               (connected ?start ?end)
                               (not (ghostAt ?end)))
            :effect (and (not (at ?start))
                         (at ?end)
                         (not (foodAt ?end))
                         (when (capsuleAt ?end)
                               (and (superPacman)
                                    (not (capsuleAt ?end))
                                    ))))

;; superpacman can move to any position if is next to the current position
;; regardless of ghost. position is updated. food, ghosts and capsules are all
;; eaten

(:action supermove
            :parameters (?start - node ?end - node)
            :precondition (and (at ?start) 
                               (connected ?start ?end)
                               (superPacman))
            :effect (and (not (at ?start))
                         (at ?end)
                         (not (foodAt ?end))
                         (not (ghostAt ?end))
                         (not (capsuleAt ?end)))))