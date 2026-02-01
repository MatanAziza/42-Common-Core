/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   atol.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/02 12:27:19 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:23:53 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_errors.h"
#include "ft_strings.h"
#include <limits.h>
// This function might need to only skip spaces.
static int	ft_isspace(int c)
{
	return (c == ' ' || c == '\f' || c == '\n' || c == '\r' || c == '\t'
		|| c == '\v');
}

static void	set_sign(const char **ptr, long *sign)
{
	if (**ptr == '+')
		(*ptr)++;
	else if (**ptr == '-')
	{
		(*ptr)++;
		*sign = -1;
	}
}

static void	init(long *sign, int *idx, t_conversion_result *result)
{
	*sign = 1;
	result->err = 0;
	result->value = 0;
	*idx = 0;
}

t_conversion_result	ft_atol(const char *nptr)
{
	long				sign;
	int					idx;
	const char			*start;
	t_conversion_result	result;

	init(&sign, &idx, &result);
	while (ft_isspace(*nptr))
		nptr++;
	set_sign(&nptr, &sign);
	start = nptr;
	while (ft_isdigit(*nptr))
		nptr++;
	if (*(nptr) != 0 || nptr == start)
	{
		result.err = 1;
		return (result);
	}
	while (nptr > start)
		increase_value(&nptr, &result, &idx);
	result.value *= sign;
	return (result);
}
