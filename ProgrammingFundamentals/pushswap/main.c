/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 15:47:18 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:41:28 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "bench.h"
#include "ft_algorithms.h"
#include "ft_output.h"
#include "ft_printf.h"
#include "pushswap.h"
#include <stdlib.h>
#include <unistd.h>

void	print_output(t_output *out)
{
	t_operation_list	*curr;

	curr = out->ops;
	while (curr)
	{
		ft_printf(1, "%s\n", op_str(curr->op));
		curr = curr->next;
	}
}

void	adaptive(t_input *input, float disorder)
{
	if (disorder < 0.20)
	{
		(input->simple)++;
	}
	else if (disorder < 0.50)
		(input->medium)++;
	else
		(input->complex)++;
	if (!input->adaptive)
		(input->adaptive)++;
}

int	ft_choose_algorithm(t_input *input, float disorder, t_stack *main_stack,
		t_output *out)
{
	t_stack	*b_stack;

	b_stack = new_stack(B);
	if (input->complex + input->medium + input->simple + input->adaptive > 1)
		return (1);
	if ((!input->complex && !input->medium && !input->simple)
		|| input->adaptive)
		adaptive(input, disorder);
	if (input->complex)
		radix_sort(main_stack, b_stack, out, find_max_bit((main_stack)->size));
	else if (input->medium)
		bucket_sort(main_stack, b_stack, out, main_stack->size);
	else if (input->simple)
		minmax(main_stack, b_stack, out);
	clear_stack(&b_stack);
	return (0);
}

t_error	compute_and_run(t_stack *main_stack, t_input input)
{
	t_output	*out;
	int			*a;
	float		disorder;

	a = ft_array_values(main_stack);
	if (!a)
		return (1);
	disorder = compute_disorder(a, main_stack->size);
	out = new_output();
	if (normalize_values(main_stack) || !out)
	{
		free(out);
		return (1);
	}
	ft_choose_algorithm(&input, disorder, main_stack, out);
	optimize_ops(out);
	if (input.bench)
		ft_bench(input, out, disorder);
	print_output(out);
	clear_output(&out);
	free(a);
	return (0);
}

// We ignore the argc/argv first argument.
int	main(int argc, char **argv)
{
	t_input	input;
	t_stack	*main_stack;
	int		err;

	input = new_input_marker();
	main_stack = new_stack(A);
	err = 0;
	if (main_stack && argc > 1)
	{
		argv++;
		argc--;
		err += treat_input(argc, argv, main_stack, &input);
		if (!err)
			err += compute_and_run(main_stack, input);
	}
	else if (!main_stack)
		err++;
	if (err)
		ft_printf(2, "Error\n");
	clear_stack(&main_stack);
}
