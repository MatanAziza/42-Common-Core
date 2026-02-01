/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   split.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/28 13:34:51 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/01 15:43:26 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_memory.h"
#include "ft_strings.h"

static size_t	count_splits(char const *s, char c)
{
	size_t	pos;
	size_t	start;
	size_t	count;

	pos = 0;
	start = 0;
	count = 0;
	while (s[pos])
	{
		if (s[pos] == c)
		{
			if (pos > start)
				count++;
			start = pos + 1;
		}
		pos++;
	}
	if (start < pos)
		count++;
	return (count);
}

static char	*add_if_valid_word(const char *s, size_t pos, size_t start)
{
	char	*ptr;

	ptr = 0;
	if (pos > start)
		ptr = ft_substr(s, start, pos - start);
	return (ptr);
}

static void	init(int *pos, size_t *start, size_t *idx)
{
	*pos = -1;
	*start = 0;
	*idx = 0;
}

static size_t	append(char **list, char *ptr, size_t idx)
{
	if (ptr)
		list[idx++] = ptr;
	return (idx);
}

char	**ft_split(char const *s, char c)
{
	int		pos;
	size_t	start;
	size_t	idx;
	char	*ptr;
	char	**list;

	if (!s)
		return (0);
	list = ft_calloc(count_splits(s, c) + 1, sizeof(char *));
	if (!list)
		return (list);
	init(&pos, &start, &idx);
	while (s[++pos])
	{
		if (s[pos] == c)
		{
			ptr = add_if_valid_word(s, pos, start);
			idx = append(list, ptr, idx);
			start = pos + 1;
		}
	}
	ptr = add_if_valid_word(s, pos, start);
	idx = append(list, ptr, idx);
	list[idx] = 0;
	return (list);
}
