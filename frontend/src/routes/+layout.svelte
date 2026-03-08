<script>
	import '../app.css';
	import { page } from '$app/stores';

	const nav = [
		{ href: '/', label: 'Inicio' },
		{ href: '/jugadores', label: 'Jugadores' },
		{ href: '/equipos', label: 'Equipos' },
		{ href: '/partidos', label: 'Partidos' },
		{ href: '/goleadores', label: 'Goleadores' }
	];
</script>

<div class="min-h-screen flex flex-col">
	<!-- Navbar -->
	<nav class="bg-green-600 text-white shadow-lg">
		<div class="container mx-auto px-4">
			<div class="flex items-center justify-between h-16">
				<div class="flex items-center space-x-2">
					<span class="text-2xl">⚽</span>
					<span class="text-xl font-bold">Fútbol Manager</span>
				</div>
				<div class="flex space-x-1">
					{#each nav as item}
						<a
							href={item.href}
							class="px-4 py-2 rounded-md transition-colors {$page.url.pathname === item.href
								? 'bg-green-700 font-semibold'
								: 'hover:bg-green-500'}"
						>
							{item.label}
						</a>
					{/each}
				</div>
			</div>
		</div>
	</nav>

	<!-- Main Content -->
	<main class="flex-1 container mx-auto px-4 py-8">
		<slot />
	</main>

	<!-- Footer -->
	<footer class="bg-gray-800 text-white py-4 mt-auto">
		<div class="container mx-auto px-4 text-center">
			<p>Fútbol Manager © 2026</p>
		</div>
	</footer>
</div>
