from src.visualization.log_analysis import plot_reward_lengh
from src.visualization.log_analysis import plot_multiple_logs
# Solo log plot
# plot_reward_lengh("logs/TicTacToeEnv/deep_q_learning/logs.json", 100)
# plot_reward_lengh("logs/TicTacToeEnv/double_deep_q_learning/logs.json", 100)
# plot_reward_lengh("logs/TicTacToeEnv/double_deep_q_learning_with_experience_replay/logs.json", 500)
# plot_reward_lengh("logs/TicTacToeEnv/double_deep_q_learning_with_prioritized_experience_replay/logs.json", 100)
# plot_reward_lengh("logs/TicTacToeEnv/reinforce/logs.json", 500)
# plot_reward_lengh("logs/TicTacToeEnv/reinforce_mean_baseline/logs.json", 500)
# plot_reward_lengh("logs/TicTacToeEnv/reinforce_actor_critic/logs.json", 500)

# plot_reward_lengh("logs/BalloonPOPEnv/deep_q_learning/logs_cautious_learner.json", 500)
# plot_reward_lengh("logs/BalloonPOPEnv/double_deep_q_learning/logs.json", 100)


# plot_reward_lengh("logs/BalloonPOPEnv/reinforce/logs.json", 500)

plot_reward_lengh("logs/BalloonPOPEnv/ppo_a2c/logs.json", 500)



# Multi logs plot
log_paths = ['logs/TicTacToeEnv/deep_q_learning/logs_balanced_strategist.json',
            'logs/TicTacToeEnv/deep_q_learning/logs_bold_explorer.json',
            "logs/TicTacToeEnv/deep_q_learning/logs_cautious_learner.json",
            "logs/TicTacToeEnv/deep_q_learning/logs.json"]

plot_multiple_logs(log_paths, 100)
