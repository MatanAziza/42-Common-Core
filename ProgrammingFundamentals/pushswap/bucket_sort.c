/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   medium_algorithms.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/04 18:28:05 by maziza            #+#    #+#             */
/*   Updated: 2025/12/04 18:31:03 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_algorithms.h"
#include "ft_printf.h"
#include "ft_stack.h"

void	minmax_bucket(t_stack *a, t_stack *b, t_output *out, int index_max)
{
	t_position	order;

	while (b->size)
	{
		order = order_rotation(b, index_max - 1);
		while (b->head->idx != (unsigned long)index_max - 1)
		{
			if (order == R)
				rotate(b, out);
			else
				reverse_rotate(b, out);
		}
		push(b, a, out);
		index_max--;
	}
}

int	ft_sqrt(int x)
{
	int	max;

	max = 0;
	while (max * max <= x)
		max += 1;
	return (max);
}

t_position	where_to_go(t_stack *a, unsigned long i_min, unsigned long i_max)
{
	long	i;
	int		dir;

	i = 0;
	dir = (int)a->size / 2;
	while (++i <= (long)a->size / 2)
	{
		if (i_min <= a->head->idx && a->head->idx < i_max && i <= ABS(dir))
			dir = i;
		rotate(a, NULL);
	}
	while (--i)
		reverse_rotate(a, NULL);
	while (++i <= (long)a->size / 2)
	{
		if (i_min <= a->head->idx && a->head->idx < i_max && i <= ABS(dir))
			dir = -i;
		reverse_rotate(a, NULL);
	}
	while (--i)
		rotate(a, NULL);
	if (dir > 0)
		return (R);
	return (RR);
}

void	push_buckets(t_stack *a, t_stack *b, t_output *out, long n)
{
	long		number_of_action;
	t_position	way;

	number_of_action = n;
	if ((long)a->size - n < 0)
		number_of_action = a->size;
	way = where_to_go(a, a->size - number_of_action, a->size - number_of_action
			+ n);
	while (number_of_action)
	{
		if (a->size - number_of_action <= a->head->idx && a->head->idx < a->size
			- number_of_action + n)
		{
			push(a, b, out);
			number_of_action--;
		}
		else
		{
			if (way == R)
				rotate(a, out);
			else
				reverse_rotate(a, out);
		}
	}
}

void	bucket_sort(t_stack *a, t_stack *b, t_output *out, long a_size)
{
	long	n;
	int		bucket_number;

	bucket_number = ft_sqrt(a_size);
	n = bucket_number;
	while (bucket_number-- > 1)
	{
		push_buckets(a, b, out, n);
		a_size -= n;
	}
	minmax_bucket(a, b, out, b->size);
}
