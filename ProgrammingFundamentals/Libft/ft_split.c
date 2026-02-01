/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <maziza@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 11:04:38 by maziza            #+#    #+#             */
/*   Updated: 2025/11/13 21:19:06 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_nb_words(const char *s, char c)
{
	int	i;
	int	count;

	i = 1;
	count = 0;
	if (!s[0])
		return (0);
	if (s[0] != c)
		count++;
	while ((char)s[i])
	{
		if ((char)s[i - 1] == c && (char)s[i] != c)
			count++;
		i++;
	}
	return (count);
}

static int	*ft_indexes(const char *s, char c, int nb_words)
{
	int	*indexes_words;
	int	i;
	int	j;

	j = 0;
	indexes_words = malloc(sizeof(int) * (nb_words + 1));
	if (!indexes_words)
		return (NULL);
	if (!s[0])
	{
		indexes_words[0] = -1;
		return (indexes_words);
	}
	i = 1;
	if ((char)s[0] != c)
		indexes_words[j++] = 0;
	while ((char)s[i])
	{
		if ((char)s[i - 1] == c && (char)s[i] != c)
			indexes_words[j++] = i;
		i++;
	}
	indexes_words[j] = -1;
	return (indexes_words);
}

static char	*ft_fill_tab(const char *s, char c, int index)
{
	int		i;
	int		len;
	char	*word;

	i = 0;
	len = 0;
	while (s[index + len] != c && s[index + len] != '\0')
		len++;
	word = malloc(len + 1);
	if (!word)
		return (NULL);
	while (s[index + i] != c && s[index + i] != '\0')
	{
		word[i] = s[index + i];
		i++;
	}
	word[i] = '\0';
	return (word);
}

static void	*ft_frees(int *indexes, char **tab)
{
	int	i;

	i = 0;
	if (tab)
	{
		while (tab[i])
		{
			free(tab[i]);
			i++;
		}
		free(tab);
	}
	if (indexes)
		free(indexes);
	return (NULL);
}

char	**ft_split(char const *s, char c)
{
	int		nb_words;
	int		*indexes_words;
	int		i;
	char	**tab;

	nb_words = ft_nb_words(s, c);
	indexes_words = ft_indexes(s, c, nb_words);
	tab = malloc(sizeof(char *) * (nb_words + 1));
	if (!tab || !indexes_words)
		return (ft_frees(indexes_words, tab));
	i = 0;
	while (indexes_words[i] != -1)
	{
		tab[i] = ft_fill_tab(s, c, indexes_words[i]);
		if (!tab[i])
			return (ft_frees(indexes_words, tab));
		i++;
	}
	free(indexes_words);
	tab[i] = NULL;
	return (tab);
}
