<?php declare(strict_types=1);
/**
 * Aura - A powerful 4 player chess engine.
 *
 * @link <https://github.com/oxuwazet/aura> Source Code.
 * @link <https://www.chess.com/4-player-chess> 4 Player Chess Online.
 *
 * @author Oxuwazet <https://github.com/oxuwazet> Profile Page.
 *
 * @license Boost Software License 1.0 <https://www.boost.org/LICENSE_1_0.txt> The license main page.
 */

namespace Aura\Search;

use Phoenix\Zero\FourPlayerChess\Utils;
use Phoenix\Zero\FourPlayerChess\Game;
use Aura\Evaluator\Evaluator;

/**
 * The minimax search.
 */
final class MinimaxSearch implements Evaluator
{
    /**
     * @var Evaluator $evaluator The evaluator instance to use.
     */
    private $evaluator;

    /**
     * @var int $depth The search depth.
     */
    private $depth;

    /**
     * Construct the minimax search.
     *
     * @param Evaluator $evaluator The evaluator instance to use.
     * @param int       $depth     The search depth.
     *
     * @return void Returns nothing.
     */
    public function __construct(Evaluator $evaluator, int $depth)
    {
        $this->evaluator = $evaluator;
        $this->depth = $depth;
    }

    /**
     * Get the best possible move.
     *
     * @return array The to and from squares for the best move.
     */
    public function bestMove(): ?array
    {
        Utils::startTransaction();
        $castleMoves = Mover::castleMoves(Utils::$move);
        $kingMoves   = Mover::kingMoves(Utils::$move);
        $queenMoves  = Mover::queenMoves(Utils::$move);
        $bishopMoves = Mover::bishopMoves(Utils::$move);
        $rookMoves   = Mover::rookMoves(Utils::$move);
        $knightMoves = Mover::knightMoves(Utils::$move);
        $pawnMoves   = Mover::pawnMoves(Utils::$move);
        $allMoves = [
            $castleMoves,
            $kingMoves,
            $queenMoves,
            $bishopMoves,
            $rookMoves,
            $knightMoves,
            $pawnMoves,
        ];
        $possiblePromotionSquares = [
            'Q',
            'R',
            'B',
            'N',
        ];
        if (Utils::$move == 'R' || Utils::$move == 'Y') {
            $bestValue = 99999;
        } else {
            $bestValue = -99999;
        }
        $bestMove = null;
        foreach ($allMoves as $sections) {
            foreach ($sections as $from => $toData) {
                foreach ($toData as $location_a) {
                    if (is_array($location_a)) {
                        $location_a = $location_a[0];
                    }
                    $to = $location_a;
                    if ($info['piece'] == 'P' && Utils::isPromotionSquare($to)) {
                        foreach ($possiblePromotionSquares as $promotionPiece) {
                            if (Move::move($from, $to, $promotionPiece, false)) {
                                $newValue = $this->search($this->depth - 1, -100000, 100000);
                                if (Utils::$move == 'R' || Utils::$move == 'Y') {
                                    if ($newValue < $bestValue) {
                                        $bestMove = [
                                            $from,
                                            $to,
                                        ];
                                        $bestValue = $newValue;
                                    }
                                } else {
                                    if ($newValue > $bestValue) {
                                        $bestMove = [
                                            $from,
                                            $to,
                                        ];
                                        $bestValue = $newValue;
                                    }
                                }
                            }
                        }
                    } else {
                        if (Move::move($from, $to, '', false)) {
                            $newValue = $this->search($this->depth - 1, -100000, 100000);
                            if (Utils::$move == 'R' || Utils::$move == 'Y') {
                                if ($newValue < $bestValue) {
                                    $bestMove = [
                                        $from,
                                        $to,
                                    ];
                                    $bestValue = $newValue;
                                }
                            } else {
                                if ($newValue > $bestValue) {
                                    $bestMove = [
                                        $from,
                                        $to,
                                    ];
                                    $bestValue = $newValue;
                                }
                            }
                        }
                    }
                }
            }
        }
        Utils::rollbackTransaction();
        return $bestMove;
    }

    /**
     * Search for the best moves possible using a tree.
     *
     * @param int $depth The search depth.
     * @param int $alpha The max alpha value.
     * @param int $beta  The min beta value.
     *
     * @return int Returns the tree sum.
     */
    private function search(int $depth, int $alpha, int $beta): int
    {
        if ($depth === 0) {
            return -$this->evaluator->evaluate();
        }
        $exportData  = Game::exportData(false);
        $castleMoves = Mover::castleMoves(Utils::$move);
        $kingMoves   = Mover::kingMoves(Utils::$move);
        $queenMoves  = Mover::queenMoves(Utils::$move);
        $bishopMoves = Mover::bishopMoves(Utils::$move);
        $rookMoves   = Mover::rookMoves(Utils::$move);
        $knightMoves = Mover::knightMoves(Utils::$move);
        $pawnMoves   = Mover::pawnMoves(Utils::$move);
        $allMoves = [
            $castleMoves,
            $kingMoves,
            $queenMoves,
            $bishopMoves,
            $rookMoves,
            $knightMoves,
            $pawnMoves,
        ];
        $possiblePromotionSquares = [
            'Q',
            'R',
            'B',
            'N',
        ];
        if (Utils::$move == 'R' || Utils::$move == 'Y') {
            $bestValue = 99999;
            foreach ($allMoves as $sections) {
                foreach ($sections as $from => $toData) {
                    foreach ($toData as $location_a) {
                        if (is_array($location_a)) {
                            $location_a = $location_a[0];
                        }
                        $to = $location_a;
                        if ($info['piece'] == 'P' && Utils::isPromotionSquare($to)) {
                            foreach ($possiblePromotionSquares as $promotionPiece) {
                                if (Move::move($from, $to, $promotionPiece, false)) {
                                    $bestValue = min($bestValue, $this->search($depth - 1, $alpha, $beta));
                                    $beta = min($beta, $bestValue);
                                    if ($beta <= $alpha) {
                                        return $bestValue;
                                    }
                                }
                                Game::importData($exportData);
                            }
                        } else {
                            if (Move::move($from, $to, '', false)) {
                                $bestValue = min($bestValue, $this->search($depth - 1, $alpha, $beta));
                                $beta = min($beta, $bestValue);
                                if ($beta <= $alpha) {
                                    return $bestValue;
                                }
                            }
                            Game::importData($exportData);
                        }
                    }
                }
            }
        } else {
            $bestValue = -99999;
            foreach ($allMoves as $sections) {
                foreach ($sections as $from => $toData) {
                    foreach ($toData as $location_a) {
                        if (is_array($location_a)) {
                            $location_a = $location_a[0];
                        }
                        $to = $location_a;
                        if ($info['piece'] == 'P' && Utils::isPromotionSquare($to)) {
                            foreach ($possiblePromotionSquares as $promotionPiece) {
                                if (Move::move($from, $to, $promotionPiece, false)) {
                                    $bestValue = max($bestValue, $this->search($depth - 1, $alpha, $beta));
                                    $beta = min($beta, $bestValue);
                                    if ($beta <= $alpha) {
                                        return $bestValue;
                                    }
                                }
                                Game::importData($exportData);
                            }
                        } else {
                            if (Move::move($from, $to, '', false)) {
                                $bestValue = max($bestValue, $this->search($depth - 1, $alpha, $beta));
                                $alpha = max($alpha, $bestValue);
                                if ($beta <= $alpha) {
                                    return $bestValue;
                                }
                            }
                            Game::importData($exportData);
                        }
                    }
                }
            }
        }
        return $bestValue;
    }
}
