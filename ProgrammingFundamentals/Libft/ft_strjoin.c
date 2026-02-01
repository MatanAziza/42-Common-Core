/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <maziza@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 11:05:42 by maziza            #+#    #+#             */
/*   Updated: 2025/11/12 11:05:46 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strjoin(const char *s1, const char *s2)
{
	char	*newstr;
	size_t	lentot;
	int		i;
	int		j;

	i = 0;
	j = 0;
	lentot = ft_strlen(s1) + ft_strlen(s2) + 1;
	newstr = malloc(sizeof(char) * lentot);
	if (!newstr)
		return (NULL);
	while (s1[i])
	{
		newstr[i] = (char)s1[i];
		i++;
	}
	while (s2[j])
		newstr[i++] = s2[j++];
	newstr[i] = '\0';
	return (newstr);
}
