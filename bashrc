# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific environment
PATH="$HOME/.local/bin:$HOME/bin:$PATH"
export PATH

# User specific aliases and functions
alias ll='ls -la'
alias h='history'
alias ssh='ssh -X'
#alias rm='rm -i'


# bashrc commands bombus
export PATH="/fibus/fs2/04/con4309/code:$PATH"
alias warteschlange="squeue -u con4309"
alias queue="squeue -u con4309"
alias run="sbatch run.sh"
