/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   radix.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 13:13:36 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/08 14:32:17 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_stack.h"

void	slow_radix_sort(t_stack *a, t_stack *b, t_output *out, int max_bits)
{
	int	bit;
	int	i;
	int	initial_size;

	bit = -1;
	while (++bit < max_bits)
	{
		i = -1;
		initial_size = a->size;
		while (++i < initial_size)
		{
			if (((a->head->value >> bit) & 1) == 0)
				push(a, b, out);
			else
				rotate(a, out);
		}
		while (b->size)
			push(b, a, out);
	}
}

void	radix_sort(t_stack *a, t_stack *b, t_output *out, int max_bits)
{
	int	bit;
	int	i;
	int	initial_size;

	bit = -1;
	while (++bit < max_bits)
	{
		i = -1;
		initial_size = a->size;
		while (++i < initial_size)
		{
			if (((a->head->idx >> bit) & 1) == 0)
				push(a, b, out);
			else
				rotate(a, out);
		}
		while (b->size)
			push(b, a, out);
	}
}
