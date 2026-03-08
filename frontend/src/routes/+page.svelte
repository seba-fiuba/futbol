<script>
	let stats = [
		{ label: 'Partidos jugados', value: '0', icon: '⚽', color: 'bg-blue-500' },
		{ label: 'Jugadores', value: '0', icon: '👥', color: 'bg-green-500' },
		{ label: 'Equipos', value: '0', icon: '🏆', color: 'bg-yellow-500' },
		{ label: 'Goles totales', value: '0', icon: '🎯', color: 'bg-red-500' }
	];
</script>

<svelte:head>
	<title>Inicio - Fútbol Manager</title>
</svelte:head>

<div class="space-y-8">
	<!-- Hero Section -->
	<div class="bg-gradient-to-r from-green-600 to-green-700 rounded-lg shadow-lg text-white p-12 text-center">
		<h1 class="text-5xl font-bold mb-4">⚽ Fútbol Manager</h1>
		<p class="text-xl opacity-90">Gestiona tus partidos, equipos y jugadores en un solo lugar</p>
	</div>

	<!-- Stats Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
		{#each stats as stat}
			<div class="bg-white rounded-lg shadow-md p-6 border-l-4 border-{stat.color}">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-gray-600 text-sm font-medium">{stat.label}</p>
						<p class="text-3xl font-bold text-gray-800 mt-2">{stat.value}</p>
					</div>
					<div class="text-4xl">{stat.icon}</div>
				</div>
			</div>
		{/each}
	</div>

	<!-- Quick Actions -->
	<div class="bg-white rounded-lg shadow-md p-8">
		<h2 class="text-2xl font-bold text-gray-800 mb-6">Acciones rápidas</h2>
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
			<a
				href="/partidos/nuevo"
				class="flex items-center space-x-3 bg-green-50 hover:bg-green-100 p-4 rounded-lg border-2 border-green-200 transition-colors"
			>
				<span class="text-2xl">➕</span>
				<div>
					<p class="font-semibold text-gray-800">Registrar nuevo partido</p>
					<p class="text-sm text-gray-600">Carga los resultados</p>
				</div>
			</a>
			<a
				href="/jugadores"
				class="flex items-center space-x-3 bg-blue-50 hover:bg-blue-100 p-4 rounded-lg border-2 border-blue-200 transition-colors"
			>
				<span class="text-2xl">👥</span>
				<div>
					<p class="font-semibold text-gray-800">Ver jugadores</p>
					<p class="text-sm text-gray-600">Lista de jugadores</p>
				</div>
			</a>
			<a
				href="/goleadores"
				class="flex items-center space-x-3 bg-yellow-50 hover:bg-yellow-100 p-4 rounded-lg border-2 border-yellow-200 transition-colors"
			>
				<span class="text-2xl">🏆</span>
				<div>
					<p class="font-semibold text-gray-800">Tabla de goleadores</p>
					<p class="text-sm text-gray-600">Mejores anotadores</p>
				</div>
			</a>
		</div>
	</div>
</div>
