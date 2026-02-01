/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/27 18:56:56 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:35:29 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_errors.h"
#include "ft_stack.h"
#include "ft_strings.h"
#include "pushswap.h"
#include <stdlib.h>

int	ft_strncmp(const char *s1, const char *s2, unsigned long n)
{
	unsigned char	*src;
	unsigned char	*cmp;
	unsigned long	x;

	cmp = (unsigned char *)s2;
	src = (unsigned char *)s1;
	if (n == 0)
		return (0);
	x = 0;
	while (n && (x < n - 1) && s1[x] && s2[x])
	{
		if (src[x] != cmp[x])
			return (src[x] - cmp[x]);
		x++;
	}
	return (src[x] - cmp[x]);
}

t_input	new_input_marker(void)
{
	t_input	new;

	new.adaptive = 0;
	new.simple = 0;
	new.medium = 0;
	new.complex = 0;
	new.bench = 0;
	new.found = 0;
	return (new);
}

t_error	treat_split(char **input, t_stack *stack)
{
	t_conversion_result	conversion_result;
	t_node				*new;
	t_error				err;

	err = 0;
	if (!input)
		return (1);
	while (*input)
	{
		new = 0;
		conversion_result = ft_atol(*input);
		if (conversion_result.err)
			err = 1;
		else if (!err)
		{
			new = new_stack_member(conversion_result.value);
			if (!new)
				err = 1;
			else
				stack_add_back(stack, new);
		}
		free(*input);
		(input)++;
	}
	return (err);
}

int	flags(t_input *input, char *s, unsigned long len)
{
	if (!ft_strncmp(s, "--simple", len))
		input->simple++;
	else if (!ft_strncmp(s, "--medium", len))
		input->medium++;
	else if (!ft_strncmp(s, "--complex", len))
		input->complex++;
	else if (!ft_strncmp(s, "--adaptive", len))
		input->adaptive++;
	else if (!ft_strncmp(s, "--bench", len))
		input->bench++;
	else
		return (0);
	return (1);
}

t_error	treat_input(int argc, char **argv, t_stack *stack, t_input *input)
{
	int				i;
	unsigned long	argument_len;
	char			**split;
	t_error			err;

	i = -1;
	while (++i < argc)
	{
		input->found = 0;
		argument_len = ft_strlen(argv[i]);
		if (argument_len > 6)
		{
			input->found = flags(input, argv[i], argument_len);
			if (input->found)
				continue ;
		}
		split = ft_split(argv[i], ' ');
		err = treat_split(split, stack);
		if (split)
			free(split);
		if (err)
			return (1);
	}
	return (0);
}
