/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/18 17:41:24 by maziza            #+#    #+#             */
/*   Updated: 2025/11/18 17:41:52 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include "get_next_line.h"

char	*ft_strdup(char *s)
{
	int		len;
	int		i;
	char	*out;

	if (!s)
		return (NULL);
	len = 0;
	while (s[len])
		len++;
	out = malloc(sizeof(char) * (len + 1));
	if (!out)
		return (NULL);
	i = 0;
	while (i < len)
	{
		out[i] = s[i];
		i++;
	}
	out[i] = '\0';
	return (out);
}

int	ft_strchr(const char *s, int c)
{
	int	i;

	i = 0;
	while (s[i])
	{
		if (s[i] == (char)c)
			return (i);
		i++;
	}
	return (-1);
}

char	*ft_strjoin(t_join *str)
{
	char	*newstr;
	int		lentot;
	int		i;
	int		j;

	i = 0;
	j = 0;
	lentot = str->b1 + str->b2 + 1;
	newstr = malloc(sizeof(char) * lentot);
	if (!newstr)
		return (NULL);
	while (i < str->b1)
	{
		newstr[i] = str->s1[i];
		i++;
	}
	while (j < str->b2)
		newstr[i++] = str->s2[j++];
	newstr[i] = '\0';
	free(str->s1);
	free(str->s2);
	return (newstr);
}

char	*ft_substr(char *s, unsigned int start, size_t len)
{
	char	*str;
	size_t	i;

	str = malloc(sizeof(char) * (len + 1));
	i = 0;
	if (!str)
		return (NULL);
	while (i < len && s[i])
	{
		str[i] = (char)s[(size_t)start + i];
		i++;
	}
	str[i] = '\0';
	free(s);
	return (str);
}

int	ft_strcpy(char *dest, char *src)
{
	int	i;

	i = 0;
	while (src[i])
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = '\0';
	return (i);
}
