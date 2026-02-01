/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <maziza@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 11:09:53 by maziza            #+#    #+#             */
/*   Updated: 2025/11/12 11:09:54 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_start(char const *s1, char const *set)
{
	int	i;
	int	j;

	i = 0;
	j = 0;
	while (set[i] && s1[j])
	{
		if (set[i] == s1[j])
		{
			i = 0;
			j++;
		}
		else
			i++;
	}
	return (j);
}

static int	ft_end(char const *s1, char const *set)
{
	int	i;
	int	j;

	j = ft_strlen(s1) - 1;
	i = 0;
	while (set[i] && j >= 0)
	{
		if (set[i] == s1[j])
		{
			i = 0;
			j--;
		}
		else
			i++;
	}
	return (j);
}

char	*ft_strtrim(char const *s1, char const *set)
{
	int		start;
	int		end;
	int		i;
	char	*newstr;

	if (!s1)
		return (NULL);
	start = ft_start(s1, set);
	if ((size_t)start == ft_strlen(s1))
		return (ft_calloc(1, 1));
	end = ft_end(s1, set);
	newstr = malloc(sizeof(char) * (end - start + 2));
	if (!newstr)
		return (NULL);
	i = 0;
	while (start + i <= end)
	{
		newstr[i] = (char)s1[start + i];
		i++;
	}
	newstr[i] = '\0';
	return (newstr);
}
