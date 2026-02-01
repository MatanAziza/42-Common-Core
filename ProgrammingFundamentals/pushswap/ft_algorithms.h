/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_algorithms.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/02 13:20:09 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:20:25 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_ALGORITHMS_H
# define FT_ALGORITHMS_H

# include "ft_errors.h"
# include "ft_stack.h"

# ifndef ABS
#  define ABS(x) (x>0 ? x : -x)
# endif
// Algorithms used for actual sorting :
//-------------------------------------
void		bucket_sort(t_stack *a, t_stack *b, t_output *out,
				long a_size);
void		minmax_bucket(t_stack *a, t_stack *b, t_output *out,
				int index_max);

void		minmax(t_stack *a, t_stack *b, t_output *out);

// A fast radix sort applied to normalized indexes (pre-sorting).
// `max_bits`always corresponds,
// for a stack containing `N` elements, to the MSB of `N-1`.
void		radix_sort(t_stack *a, t_stack *b, t_output *out, int max_bits);

//-----------------------------------------------------------------------------
//
// Optimization passes :
// ---------------------

// A slow radix sort to do indexing over values.
void		slow_radix_sort(t_stack *a, t_stack *b, t_output *out,
				int max_bits);
// A normalizing function cloning the stack and sorting it to append indexes,
// leaving it in the same order as before but with proper indexing.
t_error		normalize_values(t_stack *stack);
// Find the index of the most significant bit for a number `value`. Starts
// at bit = `0` for `0` or `1`.
int			find_max_bit(unsigned long value);
// Find whether rotate or reverse rotate is faster to get to a
// specified index value.
t_position	order_rotation(t_stack *stack, unsigned long idx);
#endif
