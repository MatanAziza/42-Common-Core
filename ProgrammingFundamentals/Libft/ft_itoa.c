/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <maziza@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/05 14:13:32 by maziza       #+#    #+#             */
/*   Updated: 2025/11/05 15:58:36 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_power(int nb, int power)
{
	if (power < 0)
		return (0);
	else if (nb == 0)
	{
		if (power == 0)
			return (1);
		return (0);
	}
	else if (power == 0)
		return (1);
	while (power > 1)
		return (nb * ft_power(nb, power - 1));
	return (nb);
}

static int	ft_lenint(long n)
{
	int	len;

	len = 0;
	if (n == 0)
		return (1);
	while (n)
	{
		n /= 10;
		len++;
	}
	return (len);
}

static void	ft_mods(char *str, long n, int len, int neg)
{
	int	i;
	int	pow;

	i = 0;
	pow = ft_power(10, len - 1);
	if (neg)
		str[i] = '-';
	while (i < len)
	{
		str[i + neg] = (n / (long)pow) % 10 + '0';
		pow /= 10;
		i++;
	}
	str[i + neg] = '\0';
}

char	*ft_itoa(int n)
{
	long	cp;
	int		len;
	char	*str;

	cp = n;
	n = 0;
	if (cp < 0)
	{
		cp = -cp;
		n = 1;
	}
	len = ft_lenint(cp);
	str = malloc(sizeof(char) * (n + len + 1));
	if (!str)
		return (ft_calloc(1, 1));
	ft_mods(str, cp, len, n);
	return (str);
}
