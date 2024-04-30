model_path=NousResearch/Meta-Llama-3-8B-Instruct
dataset_name=cellosaurus_train.json
out_dir=cellosaurus_llama3_8b_ft

python3 ./tmp_script/qlora/qlora.py \
    --model_name_or_path $model_path \
    --output_dir $out_dir \
    --eval_dataset_size 200 \
    --eval_steps 20 \
    --source_max_len 2048 \
    --target_max_len 2048 \
    --max_new_tokens 2048 \
    --dataset $dataset_name \
    --dataset_format input-output\
    --max_steps 4000 \
    --use_auth \
    --logging_steps 20 \
    --save_strategy steps \
    --data_seed 42 \
    --save_steps 40 \
    --save_total_limit 40 \
    --dataloader_num_workers 1 \
    --group_by_length \
    --logging_strategy steps \
    --remove_unused_columns False \
    --do_train \
    --lora_r 64 \
    --lora_alpha 16 \
    --lora_modules all \
    --double_quant \
    --quant_type nf4 \
    --bf16 \
    --warmup_ratio 0.03 \
    --lr_scheduler_type constant \
    --gradient_checkpointing \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 16 \
    --learning_rate 0.00005 \
    --adam_beta2 0.999 \
    --max_grad_norm 0.3 \
    --lora_dropout 0.1 \
    --weight_decay 0.0 \
    --seed 0 \
    --use_peft \
    --batch_size 4 \
    --gradient_accumulation_steps 2 \
    --evaluation_strategy steps \
    --do_eval 
