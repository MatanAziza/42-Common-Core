/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/10 12:56:37 by maziza            #+#    #+#             */
/*   Updated: 2025/11/14 13:44:32 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_check_flag(char c)
{
	if (c == 'c' || c == 's' || c == 'd' || c == 'i' || c == 'u' || c == 'x'
		|| c == 'X' || c == '%' || c == 'p')
		return (1);
	else
		return (0);
}

int	ft_redirect(int fd, const char *flag, va_list list)
{
	if (flag[1] == 'c')
		return (ft_putchar(fd, (char)va_arg(list, int)));
	else if (flag[1] == 's')
		return (ft_putstr(fd, (char *)va_arg(list, char *)));
	else if (flag[1] == 'd')
		return (ft_putnbr_base(fd, va_arg(list, int), "0123456789", 1));
	else if (flag[1] == 'i')
		return (ft_putnbr_base(fd, va_arg(list, int), "0123456789", 1));
	else if (flag[1] == 'u')
		return (ft_putnbr_base(fd, va_arg(list, unsigned int), "0123456789",
				0));
	else if (flag[1] == 'x')
		return (ft_putnbr_base(fd, va_arg(list, unsigned int),
				"0123456789abcdef", 0));
	else if (flag[1] == 'X')
		return (ft_putnbr_base(fd, va_arg(list, unsigned int),
				"0123456789ABCDEF", 0));
	else if (flag[1] == '%')
		return (ft_putchar(fd, '%'));
	else
		return (ft_print_address(fd, (unsigned long)va_arg(list, void *),
				"0123456789abcdef"));
}

int	ft_printf(int fd, const char *flag, ...)
{
	va_list	list;
	int		count;

	count = 0;
	va_start(list, flag);
	while (*flag)
	{
		if (*flag == '%' && flag[1] && ft_check_flag(flag[1]))
		{
			count += ft_redirect(fd, flag, list);
			flag += 2;
		}
		else
		{
			count += ft_putchar(fd, flag[0]);
			flag++;
		}
	}
	va_end(list);
	return (count);
}

/*int	main(void)
{
	int	a;
	int	b;

	a = printf("vrai :%p\n", &a);
	b = ft_printf("faux : %p\n", &a);
	printf("Vrai : %d, faux : %d\n", a, b);
	return (0);
}*/
