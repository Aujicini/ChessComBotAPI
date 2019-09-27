
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

namespace Aura\Evaluation;

use Phoenix\Zero\FourPlayerChess\Utils;

/**
 * The material balance evaluator.
 */
final class MaterialBalanceEvaluator implements Evaluator
{
    /**
     * Evaluate the material balance on a board.
     *
     * @return int Returns the evaluator sum.
     */
    public function evaluate(): int
    {
        $sum = 0;
        $difference = 25;
        $r_pawn = $r_minor_p = $r_major_p = 0;
        $b_pawn = $b_minor_p = $b_major_p = 0;
        $y_pawn = $y_minor_p = $y_major_p = 0;
        $g_pawn = $g_minor_p = $g_major_p = 0;
        foreach (Utils::$pieces as $key => $value) {
            if (!$value) {
                continue;
            }
            $color = substr($key, 0, 1);
            $piece = substr($key, 0, 1);
            $location = $value;
            if ($piece == 'P') {
                $piece = $value[1];
                $location = $value[0];
            }
            if ($color == 'R') {
                switch ($piece) {
                    case 'P':
                        $r_pawn += $difference;
                    break;
                    case 'N':
                        $r_minor_p += $difference * 2;
                    break;
                    case 'B':
                        $r_minor_p += $difference * 2;
                    break;
                    case 'R':
                        $r_major_p += $difference * 4;
                    break;
                    case 'Q':
                        $r_major_p += $difference * 4;
                    break;
                }
            } elseif ($color == 'Y') {
                switch ($piece) {
                    case 'P':
                        $y_pawn += $difference;
                    break;
                    case 'N':
                        $y_minor_p += $difference * 2;
                    break;
                    case 'B':
                        $y_minor_p += $difference * 2;
                    break;
                    case 'R':
                        $y_major_p += $difference * 4;
                    break;
                    case 'Q':
                        $y_major_p += $difference * 4;
                    break;
                }
            } elseif ($color == 'B') {
                switch ($piece) {
                    case 'P':
                        $b_pawn += $difference;
                    break;
                    case 'N':
                        $b_minor_p += $difference * 2;
                    break;
                    case 'B':
                        $b_minor_p += $difference * 2;
                    break;
                    case 'R':
                        $b_major_p += $difference * 4;
                    break;
                    case 'Q':
                        $b_major_p += $difference * 4;
                    break;
                }
            } else {
                switch ($piece) {
                    case 'P':
                        $g_pawn += $difference;
                    break;
                    case 'N':
                        $g_minor_p += $difference * 2;
                    break;
                    case 'B':
                        $g_minor_p += $difference * 2;
                    break;
                    case 'R':
                        $g_major_p += $difference * 4;
                    break;
                    case 'Q':
                        $g_major_p += $difference * 4;
                    break;
                }
            }
        }
        $total = $r_pawn + $r_minor_p + $r_major_p;
        $total2 = $y_pawn + $y_minor_p + $y_major_p;
        if ($total > $total2) {
            $sum += -($total - $total2);
        } elseif ($total < $total2) {
            $sum += -($total2 - $total);
        } else {
            $sum += 0;
        }
        $total = $b_pawn + $b_minor_p + $b_major_p;
        $total2 = $g_pawn + $g_minor_p + $g_major_p;
        if ($total > $total2) {
            $sum += $total - $total2;
        } elseif ($total < $total2) {
            $sum += $total2 - $total;
        } else {
            $sum += 0;
        }
        return $sum;
    }

}
