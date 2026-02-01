/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   memory.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/28 13:33:36 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/01 15:44:00 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_output.h"
#include <stddef.h>
#include <stdlib.h>

void	*ft_memset(void *s, int c, size_t n)
{
	unsigned char	*ptr;

	ptr = (unsigned char *)s;
	while (n-- != 0)
		ptr[n] = c;
	return (s);
}

void	ft_bzero(void *s, size_t n)
{
	ft_memset(s, 0, n);
}

void	*ft_calloc(size_t nmemb, size_t size)
{
	size_t	underflow;
	void	*ptr;
	size_t	allocated_size;

	ptr = 0;
	underflow = 0;
	if (nmemb == 0 || size == 0)
		allocated_size = 0;
	else if ((underflow - 1) / nmemb >= size)
		allocated_size = nmemb * size;
	else
		return (0);
	ptr = malloc(allocated_size);
	if (!ptr)
		return (0);
	ft_bzero(ptr, allocated_size);
	return (ptr);
}

void	clear_output(t_output **out)
{
	t_operation_list	*node;
	t_operation_list	*next;

	if (out && *out)
	{
		node = (*out)->ops;
		while (node)
		{
			next = node->next;
			free(node);
			node = next;
		}
		free(*out);
		*out = 0;
	}
}
