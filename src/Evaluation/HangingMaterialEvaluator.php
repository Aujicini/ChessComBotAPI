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
use Phoenix\Zero\FourPlayerChess\Threat;

/**
 * The hanging material evaluator.
 */
final class HangingMaterialEvaluator implements Evaluator
{
    /**
     * Evaluate the hanging material on a board.
     *
     * @return int Returns the evaluator sum.
     */
    public function evaluate(): int
    {
        $sum = 0;
        foreach (Utils::$pieces as $key => $value) {
            $color = substr($key, 0, 1);
            $piece = substr($key, 0, 1);
            $location = $value;
            if ($piece == 'P') {
                $piece = $value[1];
                $location = $value[0];
            }
            foreach (Utils::$pieces as $key2 => $value2) {
                if ($value == $value2) {
                    continue;
                }
                $color2 = substr($key2, 0, 1);
                $piece2 = substr($key2, 0, 1);
                $location2 = $value2;
                if ($piece2 == 'P') {
                    $piece2 = $value2[1];
                    $location2 = $value2[0];
                }
                if (Threat::isThreat($location2, $location)) {
                    if ($color == 'R' || $color == 'Y' && $color2 == 'R' || $color2 == 'Y') {
                        $sum += 25;
                    } elseif ($color == 'R' || $color == 'Y' && $color2 == 'G' || $color2 == 'B') {
                        $sum += -25;
                    } elseif ($color == 'B' || $color == 'G' && $color2 == 'R' || $color2 == 'Y') {
                        $sum += 25;
                    } elseif ($color == 'B' || $color == 'G' && $color2 == 'B' || $color2 == 'G') {
                        $sum += -25;
                    }
                }
            }
        }
        return $sum;
    }

}
