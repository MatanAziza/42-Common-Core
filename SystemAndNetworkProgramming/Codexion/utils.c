/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/25 13:46:25 by maziza            #+#    #+#             */
/*   Updated: 2026/06/25 14:22:46 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

void	swap(int *a, int *b, int cond)
{
	int	swap;

	if (!cond)
		return ;
	swap = *b;
	*b = *a;
	*a = swap;
}

int	check_arg_int(char *arg)
{
	int	i;

	i = 0;
	while (arg[i])
	{
		if ('0' > arg[i] || arg[i] > '9')
			return (1);
		i++;
	}
	return (0);
}
