<?php declare(strict_types=1);

namespace Aura\Evaluator;

use Aura\Chessboard;
use Aura\Evaluator;

final class CombinedEvaluator implements Evaluator
{
    /**
     * @var Evaluator[]
     */
    private $evaluators;

    public function __construct(array $evaluators)
    {
        $this->evaluators = array_map(function (Evaluator $evaluator): Evaluator {
            return $evaluator;
        }, $evaluators);
    }

    public function evaluate(Chessboard $board): int
    {
        $sum = 0;
        foreach ($this->evaluators as $evaluator) {
            $sum += $evaluator->evaluate($board);
        }

        return $sum;
    }
}
