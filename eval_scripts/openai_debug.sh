model_name="gpt-4o"
env="telecom"
run_id=$1
trait_dict="trait_dict_coherence"

fp="results/${model_name}_${env}_${trait_dict}_${run_id}.json"
echo "Running evaluation for env: $env, trait-dict: $trait_dict"
python run.py --agent-strategy tool-calling \
    --env $env \
    --model $model_name \
    --model-provider openai \
    --user-model gpt-4o \
    --user-model-provider openai \
    --user-strategy llm  \
    --max-concurrency 8 \
    --trait-dict "eval_scripts/${trait_dict}.json" \
    --result-fp $fp \
    --endpoint https://steer-stag.collinear.ai/steer_tau \
    --task-ids $run_id