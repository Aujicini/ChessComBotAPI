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

namespace Aura\Evaluator;

use Phoenix\Zero\FourPlayerChess\Utils;

/**
 * The material evaluator.
 */
final class MaterialEvaluator implements Evaluator
{
    /**
     * @var array[] $pieceValues A list of values assigned to pieces.
     */
    private $pieceValues = [
        'RP' => 100,
        'RN' => 300,
        'RB' => 400,
        'RR' => 525,
        'RQ' => 1000,
        'RK' => 100000,
        'BP' => -100,
        'BN' => -300,
        'BB' => -400,
        'BR' => -525,
        'BQ' => -1000,
        'BK' => -100000,
        'YP' => 100,
        'YN' => 300,
        'YB' => 400,
        'YR' => 525,
        'YQ' => 1000,
        'YK' => 100000,
        'GP' => -100,
        'GN' => -300,
        'GB' => -400,
        'GR' => -525,
        'GQ' => -1000,
        'GK' => -100000,
    ];

    /**
     * Evaluate the material on a board.
     *
     * @return int Returns the evaluator sum.
     */
    public function evaluate(): int
    {
        $sum = 0;
        foreach (Utils::$pieces as $key => $value) {
            $color = substr($key, 0, 1);
            $piece = substr($key, 0, 1);
            if ($piece == 'P') {
                $piece = $value[1];
            }
            $sum += $this->getPieceValue($color . $piece);
        }
        return $sum;
    }

    /**
     * Get the value of the specified piece.
     *
     * @return int Returns the piece value.
     */
    private function getPieceValue(?string $piece): int
    {
        return $this->pieceValues[$piece];
    }

}
