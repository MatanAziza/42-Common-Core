/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   atol_2.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/23 20:54:54 by maziza            #+#    #+#             */
/*   Updated: 2025/12/23 20:56:29 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_errors.h"
#include <limits.h>

static int	iterative_power(long nb, long power)
{
	long	i;
	long	result;

	if (power < 0)
		return (0);
	if (power == 0)
		return (1);
	i = 1;
	result = nb;
	while (i < power)
	{
		result = result * nb;
		i++;
	}
	return (result);
}

void	increase_value(const char **ptr, t_conversion_result *result, int *idx)
{
	(*ptr)--;
	result->value += (*(*ptr) - '0') * iterative_power(10, *idx);
	(*idx)++;
	if (result->value > INT_MAX || result->value < INT_MIN)
		result->err = 1;
}
