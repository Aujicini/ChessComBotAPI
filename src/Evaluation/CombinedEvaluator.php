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

/**
 * The combined evaluator.
 */
final class CombinedEvaluator implements Evaluator
{
    /**
     * @var Evaluator[] $evaluators A list of evaluators.
     */
    private $evaluators;

    /**
     * Consturct a combined evaluator.
     *
     * @return void Returns nothing.
     */
    public function __construct(array $evaluators)
    {
        $this->evaluators = array_map(function (Evaluator $evaluator): Evaluator {
            return $evaluator;
        }, $evaluators);
    }

    /**
     * Run the evaluators.
     *
     * @return int Returns the evaluation sum.
     */
    public function evaluate(): int
    {
        $sum = 0;
        foreach ($this->evaluators as $evaluator) {
            $sum += $evaluator->evaluate();
        }
        return $sum;
    }
}
