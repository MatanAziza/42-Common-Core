/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strings.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/28 13:30:33 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:23:30 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

int	ft_isdigit(int c)
{
	return (c >= '0' && c <= '9');
}

size_t	ft_strlcpy(char *dst, const char *src, size_t size)
{
	size_t	i;

	i = 0;
	while (src[i] && i < size - 1 && size != 0)
	{
		dst[i] = src[i];
		i++;
	}
	if (size > 0)
		dst[i] = '\0';
	while (src[i])
		i++;
	return (i);
}

size_t	ft_strlen(const char *s)
{
	size_t	i;

	i = 0;
	while (s[i])
		i++;
	return (i);
}

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	size_t	min_len;
	char	*ptr;
	size_t	l;

	if (!s)
		return (0);
	min_len = 0;
	l = ft_strlen(s);
	if (l < start)
	{
		ptr = malloc(1);
		if (!ptr)
			return (ptr);
		ptr[0] = 0;
		return (ptr);
	}
	while ((s + start)[min_len] && min_len < len)
	{
		min_len++;
	}
	ptr = malloc(min_len + 1);
	if (!ptr)
		return (ptr);
	ft_strlcpy(ptr, s + start, min_len + 1);
	return (ptr);
}
