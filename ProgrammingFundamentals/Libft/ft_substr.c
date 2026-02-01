/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <maziza@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 11:10:00 by maziza            #+#    #+#             */
/*   Updated: 2025/11/12 11:10:01 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_substr(const char *s, unsigned int start, size_t len)
{
	char	*str;
	size_t	i;
	size_t	lens;

	lens = ft_strlen((char *)s);
	if (start > lens)
		return ((char *)ft_calloc(1, 1));
	while (start + len > lens)
		len--;
	str = malloc(sizeof(char) * (len + 1));
	i = 0;
	if (!str)
		return (NULL);
	while (i < len && (char)s[i])
	{
		str[i] = (char)s[(size_t)start + i];
		i++;
	}
	str[i] = '\0';
	return (str);
}
