import os
from flask import Flask, render_template, jsonify
from supabase_client import supabase
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/api/trades')
def get_trades():
    trades = supabase.table('trade_history').select('*').execute()
    return jsonify(trades.data)

@app.route('/api/trades/<date>')
def get_trades_by_date(date):
    trades = supabase.table('trade_history').select('*').filter('time', 'eq', date).execute()
    return jsonify(trades.data)

@app.route('/api/metrics')
def get_metrics():
    trades = supabase.table('trade_history').select('*').execute().data
    metrics = calculate_metrics(trades)
    return jsonify(metrics)

def calculate_metrics(trades):
    profits = [trade['profit'] for trade in trades]
    gross_profit = sum(p for p in profits if p > 0)
    gross_loss = sum(p for p in profits if p < 0)
    total_net_profit = gross_profit + gross_loss
    profit_factor = gross_profit / abs(gross_loss) if gross_loss != 0 else np.inf
    expected_payoff = total_net_profit / len(trades) if trades else 0
    recovery_factor = total_net_profit / (max_drawdown(profits) or 1)
    sharpe_ratio = np.mean(profits) / (np.std(profits) or 1) if profits else 0
    balance_drawdown = max_drawdown(profits)
    
    win_trades = [p for p in profits if p > 0]
    loss_trades = [p for p in profits if p < 0]
    total_trades = len(trades)
    short_trades = [trade for trade in trades if trade['type'] == 'short']
    long_trades = [trade for trade in trades if trade['type'] == 'long']
    short_wins = [trade for trade in short_trades if trade['profit'] > 0]
    long_wins = [trade for trade in long_trades if trade['profit'] > 0]
    
    metrics = {
        "total_net_profit": total_net_profit,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor,
        "expected_payoff": expected_payoff,
        "recovery_factor": recovery_factor,
        "sharpe_ratio": sharpe_ratio,
        "balance_drawdown": balance_drawdown,
        "total_trades": total_trades,
        "short_trades": len(short_trades),
        "short_wins": len(short_wins),
        "long_trades": len(long_trades),
        "long_wins": len(long_wins),
        "short_trades_won_percentage": len(short_wins) / len(short_trades) * 100 if short_trades else 0,
        "long_trades_won_percentage": len(long_wins) / len(long_trades) * 100 if long_trades else 0,
        "profit_trades_percentage": len(win_trades) / total_trades * 100 if total_trades else 0,
        "loss_trades_percentage": len(loss_trades) / total_trades * 100 if total_trades else 0,
        "largest_profit_trade": max(win_trades, default=0),
        "largest_loss_trade": min(loss_trades, default=0),
        "average_profit_trade": np.mean(win_trades) if win_trades else 0,
        "average_loss_trade": np.mean(loss_trades) if loss_trades else 0,
        "max_consecutive_wins": max_consecutive(win_trades),
        "max_consecutive_losses": max_consecutive(loss_trades),
    }

    return metrics

def max_drawdown(profits):
    """Calculate the maximum drawdown."""
    peak = profits[0]
    drawdown = 0
    for p in profits:
        peak = max(peak, p)
        drawdown = max(drawdown, peak - p)
    return drawdown

def max_consecutive(trades):
    """Calculate the maximum number of consecutive wins/losses."""
    max_count = 0
    count = 0
    for trade in trades:
        if trade > 0:
            count += 1
        else:
            count = 0
        max_count = max(max_count, count)
    return max_count

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
