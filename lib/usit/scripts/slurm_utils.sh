### A collection of useful bash functions for working with slurm
### $Id: slurm_utils.sh,v 1.2 2013/08/20 08:44:44 bhm Exp $

## Usage      : slurm_time_secs $timestring [varname]
## Purpose    : Convert a slurm time string to #seconds
## Parametres : A slurm time string (d-h:m:s or h:m:s), an optional variable name
## Returns    : Stores the number of seconds in the global named variable,
##            : or echoes it if no variable name is specified
## Throws     : Error if it cannot parse the string
function slurm_time_secs {
    local timestring=$1
    local __varname=$2

    if [[ $timestring =~ ^(([[:digit:]]+)-)?([[:digit:]]+):([[:digit:]]+):([[:digit:]]+)$ ]]
    then
        ## Set days to 0 if unspecified (string was hh:mm:ss):
        if [[ -n ${BASH_REMATCH[2]} ]]; then
            local days=${BASH_REMATCH[2]}
        else
            local days=0
        fi

        local seconds=$(( (( 10#$days * 24 + 10#${BASH_REMATCH[3]} ) * 60 +
                           10#${BASH_REMATCH[4]} ) * 60 + 10#${BASH_REMATCH[5]}))

        ## Either set the global variable given in $2 or echo the result:
        if [[ -n $__varname ]]; then
            eval $__varname=$seconds
        else
            echo $seconds
        fi
    else
        echo "Error: $FUNCNAME: could not parse time string '$1'." >&2
        exit 1
    fi
}

## Usage      : is_notur_proj $proj_name
## Purpose    : Check if a project is a Notur project
## Parametres : The project name
## Returns    : Exits with status 0 if it is a Notur project and 1 otherwise
## Throws     : Error if it cannot parse the string
## Details    : Current implementation only uses the project name,
##              and assumes that a project is a Notur project iff its name
##              is nnXXXXk or xaXXXXk, where X is a digit.
function is_notur_proj {
    ## Compare the lowercase version of the input with a suitable regexp:
    [[ ${1,,*} =~ ^(nn|xa)[[:digit:]]{4}k$ ]]
}
